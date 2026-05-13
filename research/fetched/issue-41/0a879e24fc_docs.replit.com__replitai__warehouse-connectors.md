Skip to main content

[Replit home page](/getting-started/intro-replit)

English

  * [Docs](/getting-started/intro-replit)
  * [Tutorials](/tutorials/effective-prompting)
  * [Trust & Billing](/category/billing)
  * [Enterprise](/category/teams)
  * [Changelog](/updates/2026/05/08/changelog)
  * [Learn](https://learn.replit.com)



Search...

⌘K

  * [Start Building](https://replit.com?ref=docs)



[Replit home page](/getting-started/intro-replit)

Search or ask...

Navigation

Connectors

Data Connectors




##### Enterprise

  * [Overview](/category/teams)
  * [Information Security](/teams/information-security/overview)
  * Connectors

    * [Manage Connectors](/replitai/managing-connectors)
    * [Data Connectors](/replitai/warehouse-connectors)
    * [Connect Snowflake](/teams/snowflake-connector)
  * Developer Integrations

  * Identity and Access Management

  * Design Systems & Templates

  * [Privacy Settings](/teams/enterprise-privacy-settings)



##### Billing for Enterprise

  * [Introduction](/billing/teams-billing/overview)
  * [Managing Seats](/billing/teams-billing/managing-seats)
  * [Analytics Dashboard](/billing/teams-billing/analytics-dashboard)
  * [Cancellation](/billing/teams-billing/cancellation)



Connectors

# Data Connectors

Copy page

Connect Replit Agent to data warehouses (BigQuery, Databricks, Snowflake) and analytics platforms (Segment, Amplitude, Hex) to build data-driven applications.

Copy page

> ## Documentation Index
> 
> Fetch the complete documentation index at: <https://docs.replit.com/llms.txt>
> 
> Use this file to discover all available pages before exploring further.

Data Connectors let Replit Agent securely access your organization’s data warehouses and analytics platforms. Build powerful, data-driven applications using natural language, with centralized admin control and role-based access.

## 

​

Supported data sources

### 

​

Data warehouses (Enterprise)

Warehouse connectors are available on Enterprise plans with centralized admin control and role-based access.

  * **BigQuery**
  * **Databricks**
  * **Snowflake**

These connectors allow Agent to write and execute SQL queries against your data. You can build internal dashboards, data visualization tools, reporting systems, and applications that integrate directly with your warehouse data.

### 

​

Analytics and data platforms (all plans)

These connectors are available on Core and Pro plans. Connect your analytics and data tools so Agent can read and work with your product data.

  * **Segment** : Access customer data, event streams, and audience segments from your CDP
  * **Amplitude** : Query product analytics, user behavior data, and engagement metrics
  * **Hex** : Connect to collaborative data notebooks and query results



## 

​

Admin setup

Administrators must configure warehouse connectors before team members can use them. The setup process involves configuring an OAuth application in your warehouse provider and adding those credentials to Replit.

### 

​

Prerequisites

  * Enterprise plan (for warehouse connectors)
  * Admin access to your Replit organization
  * Ability to create OAuth applications in your warehouse provider (or access to credentials from your IT/Data team)



### 

​

Configuration steps

1

Navigate to Integrations

Go to your organization’s settings and select the **Integrations** tab.

2

Enable Connector

Select the warehouse you want to connect (BigQuery, Databricks, or Snowflake).

3

Enter Credentials

Provide the **Client ID** and **Client Secret** for the OAuth application you created in your warehouse provider.

4

Configure Access

Use Role-Based Access Control (RBAC) to specify which members or groups can use this connector.

### 

​

Warehouse-specific configuration

Databricks

Admins can configure Databricks connections using one of two methods: **User-OAuth** or **Service Account**.**Option 1: User-OAuth** This method involves minting OAuth application tokens within Databricks.

With User-OAuth, the credentials of the user who authenticates the connection are used for all subsequent access. This means that anyone using an application created with this connection will effectively have the same permissions as the authenticating user. Ensure the authenticating user has the appropriate scope of access intended for all application users.

**Option 2: Service Account** This method involves creating a service account (Service Principal) in Databricks to connect to Replit.The service account is shared among everyone given permission to use that integration. The permissions granted to the service account in Databricks will flow to all users enabled for the integration. Scope service accounts to READ-only access on the data when possible.**Managing Access Granularity** To differentiate access levels (for example, restricting specific tables to different teams):

  1. Create multiple Service Principals in Databricks
  2. Assign specific permissions to each Service Principal
  3. Create separate integrations in Replit for each Service Principal
  4. Open access to each integration only for the allowed individuals or groups



## 

​

Builder access and login

Once an admin has enabled a connector and granted you access, you can connect to the warehouse.

### 

​

Connecting to a warehouse

When you ask Agent to use a warehouse (for example, “Query the Snowflake database…”), or when you manually add the integration, you receive a login prompt. Each warehouse requires specific information during the login or connection process:

BigQuery

**Required at login:**

  * **Project ID** : You must specify the Google Cloud Project ID you want to access.



Databricks

**Required information:**

  * **SQL Warehouse** : The specific SQL Warehouse compute resource to use.
  * **Account URL** : Your Databricks account URL.



Snowflake

**Required information:**

  * **Account ID** : Your Snowflake Account ID.

For the complete setup guide, including creating the OAuth integration and troubleshooting, see [Connect Snowflake](/teams/snowflake-connector).

### 

​

Building with warehouse data

After connecting, you can ask Agent to build applications that use your data. Agent can:

  * Build internal tools that fetch and display live data
  * Create dashboards with charts and visualizations backed by your warehouse
  * Generate SQL queries to power your application’s backend
  * Explain schema and table structures to help you understand what to build



While Agent can answer ad-hoc questions about your data, the primary purpose of Data Connectors is to enable Agent to build functional applications that leverage your organization’s data. Warehouse queries are executed directly against your instance, so make sure your OAuth scopes and database user permissions allow the necessary read and write operations.

## 

​

Connector availability

Connector| Starter| Core| Pro| Enterprise  
---|---|---|---|---  
BigQuery| —| —| —| ✅  
Databricks| —| —| —| ✅  
Snowflake| —| —| —| ✅  
Segment| —| ✅| ✅| ✅  
Amplitude| —| ✅| ✅| ✅  
Hex| —| ✅| ✅| ✅  
  
## 

​

Related documentation

  * [Workspaces](/core-concepts/workspaces): Understand Personal and Team Workspaces
  * [Connectors overview](/replitai/integrations) — Learn about all integration types
  * [Connect Snowflake](/teams/snowflake-connector) — Step-by-step Snowflake setup with OAuth configuration and troubleshooting
  * [Managing your connectors](/replitai/managing-connectors) — Connector management on collaborative workspaces in Core, on collaborative workspaces in Pro, and Enterprise



Was this page helpful?

YesNo

[Managing Your ConnectorsPrevious](/replitai/managing-connectors)[Connect SnowflakeNext](/teams/snowflake-connector)

⌘I

[x](https://x.com/replit)[linkedin](https://www.linkedin.com/company/repl-it)[youtube](https://www.youtube.com/@replit)

On this page

  * Supported data sources
  * Data warehouses (Enterprise)
  * Analytics and data platforms (all plans)
  * Admin setup
  * Prerequisites
  * Configuration steps
  * Warehouse-specific configuration
  * Builder access and login
  * Connecting to a warehouse
  * Building with warehouse data
  * Connector availability
  * Related documentation


