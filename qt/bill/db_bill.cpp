#include "db_bill.h"

#include <QMutex>
#include <QDebug>
#include <QSqlQuery>
#include <QSqlDatabase>

DB_Bill * DB_Bill::m_only = nullptr;

DB_Bill *DB_Bill::g()
{
    QMutex mutex;
    mutex.lock();
    if(m_only == nullptr){
        m_only = new DB_Bill();
    }
    mutex.unlock();
    return m_only;
}

DB_Bill::DB_Bill()
{
    m_db = QSqlDatabase::addDatabase("QSQLITE", "BILL");
    m_db.setDatabaseName("../../db/user.db");
    if(!m_db.open())  qDebug() << "db open fail!!!";
}

QSqlQuery DB_Bill::select(int _cmd)
{
    m_sql.clear();

    switch(_cmd){
    case From::CMD_USER:
        m_sql = m_db.exec("Select * from email_user");
        break;
    case From::CMD_ADMIN:
        m_sql = m_db.exec("Select * from admin");
        break;
    case From::CMD_URL:
        m_sql = m_db.exec("Select * from url");
        break;
    case From::CMD_NOW:
        m_sql = m_db.exec("Select * from now");
        break;
    case From::CMD_BILL:
        m_sql = m_db.exec("Select * from bill");
        break;
    }

    return m_sql;
}
