from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import os
import json
import sqlite3


# ========================================
# WEBSITE FOLDER
# ========================================

os.chdir(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


# ========================================
# DATABASE
# ========================================

DATABASE = "messages.db"


def create_database():

    connection = sqlite3.connect(
        DATABASE
    )

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT
        )
    """)

    connection.commit()

    connection.close()


create_database()


# ========================================
# ADMIN LOGIN
# ========================================

# Local defaults for Termux.
# On Render, these will come from environment variables.

ADMIN_USERNAME = os.environ.get(
    "ADMIN_USERNAME",
    "Iconix_Era"
)

ADMIN_PASSWORD = os.environ.get(
    "ADMIN_PASSWORD",
    "Iivon@29"
)


# ========================================
# WEBSITE SERVER
# ========================================

class WebsiteHandler(
    SimpleHTTPRequestHandler
):


    # ====================================
    # GET REQUESTS
    # ====================================

    def do_GET(self):

        parsed_url = urlparse(
            self.path
        )


        # 🐍 Python greeting

        if parsed_url.path == "/api/hello":

            query = parse_qs(
                parsed_url.query
            )

            name = query.get(
                "name",
                ["friend"]
            )[0]

            self.send_json({

                "message":
                f"Hello, {name}! 🐍🚀"

            })

            return


        # 📩 Get all messages

        if parsed_url.path == "/api/messages":

            connection = sqlite3.connect(
                DATABASE
            )

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    name,
                    email,
                    message,
                    created_at
                FROM messages
                ORDER BY id DESC
            """)

            rows = cursor.fetchall()

            connection.close()


            messages = []


            for row in rows:

                messages.append({

                    "id": row[0],

                    "name": row[1],

                    "email": row[2],

                    "message": row[3],

                    "created_at": row[4]

                })


            self.send_json(
                messages
            )

            return


        # Normal website files

        super().do_GET()


    # ====================================
    # POST REQUESTS
    # ====================================

    def do_POST(self):


        # =================================
        # 🔐 LOGIN
        # =================================

        if self.path == "/api/login":

            data = self.read_json()


            username = data.get(
                "username",
                ""
            )

            password = data.get(
                "password",
                ""
            )


            if (
                username ==
                ADMIN_USERNAME
                and
                password ==
                ADMIN_PASSWORD
            ):

                self.send_json({

                    "success":
                    True,

                    "message":
                    "Login successful."

                })

            else:

                self.send_json({

                    "success":
                    False,

                    "message":
                    "Wrong username or password."

                })

            return


        # =================================
        # 📩 CREATE MESSAGE
        # =================================

        if self.path == "/api/contact":

            data = self.read_json()


            name = data.get(
                "name",
                ""
            ).strip()

            email = data.get(
                "email",
                ""
            ).strip()

            message = data.get(
                "message",
                ""
            ).strip()


            if not name or not email or not message:

                self.send_json({

                    "success":
                    False,

                    "message":
                    "Please fill in all fields."

                })

                return


            created_at = (
                datetime.now()
                .strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )


            connection = sqlite3.connect(
                DATABASE
            )

            cursor = connection.cursor()


            cursor.execute("""
                INSERT INTO messages
                (
                    name,
                    email,
                    message,
                    created_at
                )
                VALUES (?, ?, ?, ?)
            """, (
                name,
                email,
                message,
                created_at
            ))


            connection.commit()

            connection.close()


            self.send_json({

                "success":
                True,

                "message":
                "Message sent successfully! 🚀"

            })

            return


        # =================================
        # ✏️ UPDATE MESSAGE
        # =================================

        if self.path == "/api/update-message":

            data = self.read_json()


            message_id = data.get(
                "id"
            )

            name = data.get(
                "name",
                ""
            )

            email = data.get(
                "email",
                ""
            )

            message = data.get(
                "message",
                ""
            )


            connection = sqlite3.connect(
                DATABASE
            )

            cursor = connection.cursor()


            cursor.execute("""
                UPDATE messages

                SET
                    name = ?,
                    email = ?,
                    message = ?

                WHERE id = ?
            """, (
                name,
                email,
                message,
                message_id
            ))


            connection.commit()

            connection.close()


            self.send_json({

                "success":
                True,

                "message":
                "Message updated successfully."

            })

            return


        # =================================
        # 🗑️ DELETE MESSAGE
        # =================================

        if self.path == "/api/delete-message":

            data = self.read_json()


            message_id = data.get(
                "id"
            )


            connection = sqlite3.connect(
                DATABASE
            )

            cursor = connection.cursor()


            cursor.execute(
                """
                DELETE FROM messages
                WHERE id = ?
                """,
                (
                    message_id,
                )
            )


            connection.commit()

            connection.close()


            self.send_json({

                "success":
                True,

                "message":
                "Message deleted successfully."

            })

            return


        # =================================
        # ❌ UNKNOWN POST ENDPOINT
        # =================================

        self.send_json({

            "success":
            False,

            "message":
            "API endpoint not found."

        })


    # ====================================
    # READ JSON
    # ====================================

    def read_json(self):

        length = int(
            self.headers.get(
                "Content-Length",
                0
            )
        )


        body = self.rfile.read(
            length
        )


        if not body:

            return {}


        return json.loads(
            body.decode()
        )


    # ====================================
    # SEND JSON
    # ====================================

    def send_json(
        self,
        data
    ):

        response = json.dumps(
            data
        ).encode()


        self.send_response(
            200
        )


        self.send_header(
            "Content-Type",
            "application/json"
        )


        self.send_header(
            "Content-Length",
            str(
                len(response)
            )
        )


        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )


        self.end_headers()


        self.wfile.write(
            response
        )


# ========================================
# START SERVER
# ========================================

PORT = int(
    os.environ.get(
        "PORT",
        8080
    )
)


server = HTTPServer(
    ("", PORT),
    WebsiteHandler
)


print()

print(
    "===================================="
)

print(
    "🐍 IVON PYTHON WEBSITE SERVER"
)

print(
    "===================================="
)

print(
    f"🌐 Port: {PORT}"
)

print(
    "🔐 Login: /api/login"
)

print(
    "🐍 Python: /api/hello"
)

print(
    "📩 Messages: /api/messages"
)

print(
    "✏️ Update: /api/update-message"
)

print(
    "🗑️ Delete: /api/delete-message"
)

print(
    "💾 Database: messages.db"
)

print(
    "===================================="
)

print()


server.serve_forever()
