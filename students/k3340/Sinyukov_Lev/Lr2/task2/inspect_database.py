from __future__ import annotations

from sqlalchemy import text

from db_connection import get_session, settings


def print_section(title: str) -> None:
    print()
    print(title)
    print("-" * len(title))


def format_value(value: object) -> str:
    if value is None:
        return "NULL"
    return str(value)


def print_table(rows: list[dict], empty_message: str = "No rows found.") -> None:
    if not rows:
        print(empty_message)
        return

    columns = list(rows[0].keys())
    widths: dict[str, int] = {}

    for column in columns:
        widths[column] = len(column)

    for row in rows:
        for column in columns:
            widths[column] = max(widths[column], len(format_value(row[column])))

    separator = "+-" + "-+-".join("-" * widths[column] for column in columns) + "-+"
    header = "| " + " | ".join(column.ljust(widths[column]) for column in columns) + " |"

    print(separator)
    print(header)
    print(separator)

    for row in rows:
        line = "| " + " | ".join(format_value(row[column]).ljust(widths[column]) for column in columns) + " |"
        print(line)

    print(separator)


def fetch_table_counts() -> dict[str, int]:
    with get_session() as session:
        return {
            "users": session.execute(text("SELECT COUNT(*) FROM users")).scalar_one(),
            "trips": session.execute(text("SELECT COUNT(*) FROM trips")).scalar_one(),
            "messages": session.execute(text("SELECT COUNT(*) FROM messages")).scalar_one(),
        }


def fetch_parser_user_rows() -> list[dict]:
    with get_session() as session:
        result = session.execute(
            text(
                """
                SELECT id, email, username, created_at
                FROM users
                WHERE email = :email OR username = :username
                ORDER BY id
                """
            ),
            {
                "email": settings.parser_user_email,
                "username": settings.parser_username,
            },
        )
        return [dict(row._mapping) for row in result]


def fetch_parser_trip_rows() -> list[dict]:
    with get_session() as session:
        result = session.execute(
            text(
                """
                SELECT id, owner_id, title, departure_city, destination_city, created_at
                FROM trips
                WHERE title = :title
                ORDER BY id
                """
            ),
            {"title": settings.parser_trip_title},
        )
        return [dict(row._mapping) for row in result]


def fetch_parser_message_rows() -> list[dict]:
    with get_session() as session:
        result = session.execute(
            text(
                """
                SELECT
                    messages.id,
                    messages.trip_id,
                    messages.author_id,
                    messages.content,
                    messages.created_at
                FROM messages
                JOIN users ON users.id = messages.author_id
                JOIN trips ON trips.id = messages.trip_id
                WHERE users.email = :email
                   OR users.username = :username
                   OR trips.title = :title
                ORDER BY messages.id
                """
            ),
            {
                "email": settings.parser_user_email,
                "username": settings.parser_username,
                "title": settings.parser_trip_title,
            },
        )
        return [dict(row._mapping) for row in result]


def main() -> None:
    print("Database connection check")
    print(f"DATABASE_URL: {settings.database_url}")

    counts = fetch_table_counts()
    print_section("Table counts")
    count_rows = [{"table_name": table_name, "row_count": count} for table_name, count in counts.items()]
    print_table(count_rows)

    print_section("Parser user rows")
    print_table(fetch_parser_user_rows(), "Parser user not found.")

    print_section("Parser trip rows")
    print_table(fetch_parser_trip_rows(), "Parser trip not found.")

    print_section("Parser message rows")
    print_table(fetch_parser_message_rows(), "Parser messages not found.")


if __name__ == "__main__":
    main()
