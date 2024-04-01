#include "bill_widget.h"

#include <QApplication>
#include <QTextCodec>
#include <QDebug>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    QTextCodec *pText=QTextCodec::codecForName("UTF-8");
    QTextCodec::setCodecForLocale(pText);
    QTextCodec::setCodecForCStrings(pText);
    QTextCodec::setCodecForTr(pText);

    BillWidget w;
    w.setMinimumSize(400, 600);
    w.setMaximumSize(400, 600);
//    w.setWindowFlags(Qt::FramelessWindowHint);
    w.show();
    return a.exec();
}
