import sqlite3

DATABASE = "pvc_global.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # =====================================================
    # CONTACTS TABLE
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            destination TEXT,
            subject TEXT,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # =====================================================
    # USERS TABLE
    # For Sign In / Register
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # =====================================================
    # FAQ TABLE
    # AI Knowledge Base
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            keywords TEXT,
            active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # =====================================================
    # CONVERSATIONS TABLE
    # AI Chat Sessions
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)
        )
        """
    )

    # =====================================================
    # CHAT MESSAGES TABLE
    # AI Messages
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (conversation_id)
                REFERENCES conversations(id)
        )
        """
    )

    conn.commit()
    conn.close()


# =========================================================
# CONTACT FUNCTIONS
# =========================================================

def save_contact(
    full_name,
    email,
    phone,
    destination,
    subject,
    message
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO contacts
        (
            full_name,
            email,
            phone,
            destination,
            subject,
            message
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            full_name,
            email,
            phone,
            destination,
            subject,
            message
        )
    )

    conn.commit()

    contact_id = cursor.lastrowid

    conn.close()

    return contact_id


# =========================================================
# FAQ FUNCTIONS
# =========================================================

def add_faq(
    category,
    question,
    answer,
    keywords=""
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO faqs
        (
            category,
            question,
            answer,
            keywords
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            category,
            question,
            answer,
            keywords
        )
    )

    conn.commit()
    conn.close()


def get_all_faqs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM faqs
        WHERE active = 1
        ORDER BY category, id
        """
    )

    faqs = cursor.fetchall()

    conn.close()

    return faqs


def search_faq(query):
    conn = get_connection()
    cursor = conn.cursor()

    search_term = f"%{query.lower()}%"

    cursor.execute(
        """
        SELECT *
        FROM faqs

        WHERE active = 1

        AND (
            LOWER(question) LIKE ?
            OR LOWER(answer) LIKE ?
            OR LOWER(keywords) LIKE ?
            OR LOWER(category) LIKE ?
        )

        ORDER BY id DESC

        LIMIT 5
        """,
        (
            search_term,
            search_term,
            search_term,
            search_term
        )
    )

    results = cursor.fetchall()

    conn.close()

    return results


# =========================================================
# AI CONVERSATION FUNCTIONS
# =========================================================

def create_conversation(
    user_id=None,
    session_id=None
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO conversations
        (
            user_id,
            session_id
        )
        VALUES (?, ?)
        """,
        (
            user_id,
            session_id
        )
    )

    conversation_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return conversation_id


def save_message(
    conversation_id,
    role,
    message
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_messages
        (
            conversation_id,
            role,
            message
        )
        VALUES (?, ?, ?)
        """,
        (
            conversation_id,
            role,
            message
        )
    )

    conn.commit()
    conn.close()


def get_chat_history(conversation_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            role,
            message,
            created_at
        FROM chat_messages
        WHERE conversation_id = ?
        ORDER BY id ASC
        """,
        (conversation_id,)
    )

    messages = cursor.fetchall()

    conn.close()

    return messages


# =========================================================
# INITIALIZE DATABASE
# =========================================================

if __name__ == "__main__":
    init_db()
    print("PVC Global database initialized successfully.")