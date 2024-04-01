#ifndef DB_BILL_H
#define DB_BILL_H

#include <QString>
#include <QSqlQuery>
#include <QSqlDatabase>


enum From{
    CMD_USER,
    CMD_ADMIN,
    CMD_URL,
    CMD_NOW,
    CMD_BILL
};

class DB_Bill
{
public:
    static DB_Bill * g();

private:
    static DB_Bill * m_only;

    QSqlQuery m_sql;
    QSqlDatabase m_db;
private:
    DB_Bill();

public:
    QSqlQuery select(int _cmd);
};

#endif // DB_BILL_H
