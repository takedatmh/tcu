#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ErrorCode,
  ListToolsRequestSchema,
  McpError,
} from '@modelcontextprotocol/sdk/types.js';
import pkg from 'pg';
const { Pool } = pkg;

interface ConnectionConfig {
  host: string;
  port: number;
  database: string;
  user: string;
  password: string;
}

interface QueryToolArgs {
  sql: string;
}

interface SchemaToolArgs {
  table_name?: string;
}

const isValidQueryArgs = (args: any): args is QueryToolArgs =>
  typeof args === 'object' &&
  args !== null &&
  typeof args.sql === 'string';

const isValidSchemaArgs = (args: any): args is SchemaToolArgs =>
  typeof args === 'object' &&
  args !== null &&
  (args.table_name === undefined || typeof args.table_name === 'string');

class PostgreSQLServer {
  private server: Server;
  private pool: pkg.Pool | null = null;

  constructor() {
    this.server = new Server(
      {
        name: 'postgresql-mcp-server',
        version: '0.1.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
    
    this.server.onerror = (error) => console.error('[MCP Error]', error);
    process.on('SIGINT', async () => {
      await this.cleanup();
      process.exit(0);
    });
  }

  private async cleanup() {
    if (this.pool) {
      await this.pool.end();
    }
    await this.server.close();
  }

  private getConnectionConfig(): ConnectionConfig {
    return {
      host: process.env.POSTGRES_HOST || 'localhost',
      port: parseInt(process.env.POSTGRES_PORT || '5432'),
      database: process.env.POSTGRES_DB || 'postgres',
      user: process.env.POSTGRES_USER || 'postgres',
      password: process.env.POSTGRES_PASSWORD || '',
    };
  }

  private async ensureConnection() {
    if (!this.pool) {
      const config = this.getConnectionConfig();
      this.pool = new Pool(config);
    }
    return this.pool;
  }

  private setupToolHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'get_schema',
          description: 'Get database schema information. If table_name is provided, returns detailed schema for that table. Otherwise, returns list of all tables.',
          inputSchema: {
            type: 'object',
            properties: {
              table_name: {
                type: 'string',
                description: 'Optional: specific table name to get detailed schema',
              },
            },
          },
        },
        {
          name: 'execute_query',
          description: 'Execute a SQL query on the PostgreSQL database. Use this to run SELECT queries to retrieve data. Be careful with UPDATE, INSERT, DELETE operations.',
          inputSchema: {
            type: 'object',
            properties: {
              sql: {
                type: 'string',
                description: 'The SQL query to execute',
              },
            },
            required: ['sql'],
          },
        },
        {
          name: 'get_sample_data',
          description: 'Get sample data from a table (first 10 rows)',
          inputSchema: {
            type: 'object',
            properties: {
              table_name: {
                type: 'string',
                description: 'Name of the table to get sample data from',
              },
            },
            required: ['table_name'],
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      try {
        const pool = await this.ensureConnection();

        switch (request.params.name) {
          case 'get_schema': {
            if (!isValidSchemaArgs(request.params.arguments)) {
              throw new McpError(
                ErrorCode.InvalidParams,
                'Invalid schema arguments'
              );
            }

            const tableName = request.params.arguments.table_name;

            if (tableName) {
              // Get detailed schema for specific table
              const result = await pool.query(`
                SELECT 
                  column_name,
                  data_type,
                  character_maximum_length,
                  is_nullable,
                  column_default
                FROM information_schema.columns
                WHERE table_name = $1
                ORDER BY ordinal_position;
              `, [tableName]);

              return {
                content: [
                  {
                    type: 'text',
                    text: JSON.stringify({
                      table: tableName,
                      columns: result.rows,
                    }, null, 2),
                  },
                ],
              };
            } else {
              // Get list of all tables
              const result = await pool.query(`
                SELECT 
                  table_name,
                  table_type
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
              `);

              return {
                content: [
                  {
                    type: 'text',
                    text: JSON.stringify({
                      tables: result.rows,
                    }, null, 2),
                  },
                ],
              };
            }
          }

          case 'execute_query': {
            if (!isValidQueryArgs(request.params.arguments)) {
              throw new McpError(
                ErrorCode.InvalidParams,
                'Invalid query arguments'
              );
            }

            const sql = request.params.arguments.sql;
            const result = await pool.query(sql);

            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({
                    rowCount: result.rowCount,
                    rows: result.rows,
                    fields: result.fields.map(f => ({
                      name: f.name,
                      dataTypeID: f.dataTypeID,
                    })),
                  }, null, 2),
                },
              ],
            };
          }

          case 'get_sample_data': {
            if (!isValidSchemaArgs(request.params.arguments)) {
              throw new McpError(
                ErrorCode.InvalidParams,
                'Invalid arguments'
              );
            }

            const tableName = request.params.arguments.table_name;
            if (!tableName) {
              throw new McpError(
                ErrorCode.InvalidParams,
                'table_name is required'
              );
            }

            const result = await pool.query(`
              SELECT * FROM ${tableName} LIMIT 10;
            `);

            return {
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({
                    table: tableName,
                    rowCount: result.rowCount,
                    rows: result.rows,
                  }, null, 2),
                },
              ],
            };
          }

          default:
            throw new McpError(
              ErrorCode.MethodNotFound,
              `Unknown tool: ${request.params.name}`
            );
        }
      } catch (error) {
        if (error instanceof McpError) {
          throw error;
        }
        
        const errorMessage = error instanceof Error ? error.message : String(error);
        return {
          content: [
            {
              type: 'text',
              text: `Database error: ${errorMessage}`,
            },
          ],
          isError: true,
        };
      }
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('PostgreSQL MCP server running on stdio');
  }
}

const server = new PostgreSQLServer();
server.run().catch(console.error);
