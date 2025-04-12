# Installing PostgreSQL and pgAdmin

## Installation on Windows

1. Download PostgreSQL from the official website: [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
2. Run the installer and follow the steps:
   - Select the components you want to install (keep the defaults).
   - Set up a password for the default **postgres** user.
   - Note the default port (5432) and installation directory.
3. Complete the installation and start PostgreSQL using **pgAdmin** or **SQL Shell (psql)**.
4. Download pgAdmin from [https://www.pgadmin.org/download/](https://www.pgadmin.org/download/).
5. Install pgAdmin and launch it.
6. Connect to your PostgreSQL instance by entering your credentials.

## Installation on macOS

### Using Homebrew
1. Open Terminal and run:
   ```sh
   brew install postgresql
   ```
2. Start PostgreSQL as a background service:
   ```sh
   brew services start postgresql
   ```
3. Verify installation:
   ```sh
   psql --version
   ```
4. Install pgAdmin by downloading it from [https://www.pgadmin.org/download/](https://www.pgadmin.org/download/).
5. Open pgAdmin and connect to the local PostgreSQL instance.

## Creating a Database
After installing PostgreSQL:
1. Open `psql` or connect via pgAdmin.
2. Run the following to create a database:
   ```sql
   CREATE DATABASE my_database;
   ```
3. To verify, list the databases:
   ```sql
   \l
   ```

Your PostgreSQL and pgAdmin setup is now ready!