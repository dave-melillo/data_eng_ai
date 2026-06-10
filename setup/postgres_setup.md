## Installing PostgreSQL and pgAdmin

Getting PostgreSQL and pgAdmin up and running depends on your operating system *and* your preferred setup method. Below are detailed instructions for **Windows**, **macOS** (with and without Homebrew), and **Linux**. If you run into trouble, don’t worry—we include a fallback option using Docker.

---

### 🪟 Installation on Windows

1. Download PostgreSQL from the official website:
   👉 [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
2. Run the installer and follow the steps:

   * Keep default components selected.
   * Set a password for the default `postgres` user.
   * Note the default port (`5432`) and installation path.
3. Complete the install and launch **pgAdmin** (installed by default).
4. Alternatively, you can use **SQL Shell (psql)** for command-line access.

---

### 🍎 Installation on macOS

#### Option 1: Using Homebrew (recommended if available)

1. Open Terminal and run:

   ```bash
   brew install postgresql
   ```
2. Start PostgreSQL as a background service:

   ```bash
   brew services start postgresql
   ```
3. Confirm it's running:

   ```bash
   psql --version
   ```

#### Option 2: Direct Installer (no Homebrew required)

1. Download the PostgreSQL installer from [https://www.postgresql.org/download/macosx/](https://www.postgresql.org/download/macosx/)
2. Follow the installation wizard:

   * Set a password for the `postgres` user.
   * Accept default port (`5432`) unless you have a conflict.
3. This installer includes **pgAdmin** by default.
4. After install, open **pgAdmin** to manage your instance.

---

### 🐧 Installation on Linux (Ubuntu/Debian-based)

1. Open a terminal and run:

   ```bash
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   ```
2. Start the PostgreSQL service:

   ```bash
   sudo systemctl start postgresql
   ```
3. Optionally, enable it to start on boot:

   ```bash
   sudo systemctl enable postgresql
   ```
4. Access PostgreSQL using:

   ```bash
   sudo -u postgres psql
   ```

To install **pgAdmin** on Linux, follow instructions for your distro here:
👉 [https://www.pgadmin.org/download/](https://www.pgadmin.org/download/)

---

### 🐳 Alternative: Running PostgreSQL via Docker

If you'd rather not install anything natively, Docker provides a clean and disposable option:

```bash
docker run --name my_postgres \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  -d postgres
```

You can connect to this container from pgAdmin or `psql` using:

* Host: `localhost`
* Port: `5432`
* User: `postgres`
* Password: `mysecretpassword`

---

## 🎯 Creating a Database

Once PostgreSQL is installed and running:

### Using `psql` (terminal):

```sql
CREATE DATABASE my_database;
\l  -- to list all databases
```

### Using pgAdmin:

1. Open pgAdmin and connect to your server.
2. Right-click "Databases" → *Create* → *Database*.
3. Name it `my_database` and click Save.

---

## 🎬 Loading the Pagila sample database

Chapter 3 (and the SQL examples in Chapter 2) use **Pagila**, a PostgreSQL sample database modeled on a DVD rental store. The two SQL files you need ship in the `ch02/` folder of this repository:

* `pagila-schema.sql` — creates the tables, views, and functions
* `pagila-insert-data.sql` — loads the sample data

With PostgreSQL installed and running, create a database named `pagila` and load the schema **first**, then the data. From the repository root:

```bash
# 1. Create the database
createdb pagila

# 2. Load the schema, then the data (order matters)
psql -d pagila -f ch02/pagila-schema.sql
psql -d pagila -f ch02/pagila-insert-data.sql
```

If `createdb` isn't on your path, create the database from inside `psql` (`CREATE DATABASE pagila;`) and then run the two `psql ... -f` commands above.

Confirm the load worked:

```bash
psql -d pagila -c "SELECT count(*) FROM film;"
```

You should see **1000** films. Point pgAdmin or your `psql` connection at the `pagila` database whenever a chapter calls for it.