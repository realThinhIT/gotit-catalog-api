from main import db
import logging


def execute_sql_from_file(filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sql_file = fd.read()
    fd.close()

    # All SQL commands (split on ';')
    sql_commands = sql_file.split(';')

    # Execute every command from the input file
    for command in sql_commands:
        # This will skip and report validation
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            db.session.execute(command.decode('utf-8'))
        except Exception, e:
            logging.exception(e)
