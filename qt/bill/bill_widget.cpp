#include "bill_widget.h"

#include <QDebug>
#include <QString>
#include <QProcess>
#include <QPainter>
#include <QMouseEvent>

#include "db_bill.h"

BillWidget::BillWidget(QWidget *parent)
    : QWidget(parent)
{
    m_angle         = 0;
    m_move_status   = T_None;
    m_click_status  = T_None;

    setMouseTracking(true);
    m_user                = QRect(20, 300, 360, 50 );
    m_cur_user            = QRect(                 );
    m_refresh             = QRect(                 );
    m_balance_water       = QRect(20, 100, 360, 50 );
    m_balance_electricity = QRect(20, 160, 360, 50 );

    m_color_tall      = QColor(173, 255, 47 , 255);
    m_color_centre    = QColor(255, 165, 0  , 255);
    m_color_low       = QColor(255, 0  , 0  , 255);
    m_color_cur_user  = QColor(30 , 144, 255, 255);

    m_timer_finish.setInterval( 40);
    m_timer_process.setInterval(40);
    connect(&m_timer_process, SIGNAL(timeout()), this, SLOT(s_timer_process()));
    connect(&m_timer_finish , SIGNAL(timeout()), this, SLOT(s_timer_finish( )));
    update();
}

BillWidget::~BillWidget()
{
}

void BillWidget::getColor(int _val, QColor &_color)
{
    int i_color = _val > 10 ? (_val > 15 ? 2 : 1) : 0;
    switch(i_color){
    case 0: _color = m_color_low;       break;
    case 1: _color = m_color_centre;    break;
    case 2: _color = m_color_tall;      break;
    }
}

void BillWidget::getBill(QString &_water, QString &_ele, QColor &_c_water, QColor &_c_ele)
{
//    QProcess proc(this);
//    proc.startDetached("python3 main.py");

    QSqlQuery query = DB_Bill::g()->select(From::CMD_BILL);
    while(query.next()){
        if(query.value(0).toString() == "water")               _water = query.value(1).toString();
        else if(query.value(0).toString() == "electricity")    _ele   = query.value(1).toString();
    }

    getColor(_water.toInt(), _c_water);
    getColor(_ele.toInt()  , _c_ele  );
}

void BillWidget::getUser(QMap<QString, QString> &_l_user, QString &_curr)
{
    QSqlQuery query = DB_Bill::g()->select(From::CMD_USER);
    while(query.next())     _l_user.insert(query.value(0).toString(), query.value(1).toString());

    QSqlQuery query1 = DB_Bill::g()->select(From::CMD_NOW);
    while(query1.next())     _curr = query1.value(0).toString();
}

void BillWidget::setConfig()
{

}

void BillWidget::resetDrawWindow()
{
    if(T_Complete == (m_move_status & T_Complete)){
        m_move_status = T_None;
        repaint();
    }
}

bool BillWidget::movePaint(QPainter *_pain)
{
    if(T_None != (m_move_status & T_None))    return false;

    switch(m_move_status){
    case T_Move_Curr: paintTipText(_pain);    break;
    default:    return false;
    }
        return true;

}

bool BillWidget::clickPaint(QPainter *_pain)
{
    switch(m_click_status){
    case T_Click_Refresh:
    case T_Click_Refresh | T_Complete: paintRound(_pain);  break;
    default:    return false;
    }
    return true;
}

void BillWidget::paintRound(QPainter *_pain)
{
//    int i_w = rect().width() / 2;
//    int i_h = rect().height() / 2;
//    QRadialGradient radialGradient(QPointF(i_w, i_h), i_w, QPointF(i_w, i_h));
//    radialGradient.setColorAt(0, QColor(245, 120, 220, 255));
//    radialGradient.setColorAt(1, QColor(182, 206, 232, 255));
//    _pain->setBrush(radialGradient);
//    _pain->drawRect(rect());

//    圆形刷新图
//    QLinearGradient linearGradient(rect().width(), 20, rect().width()+30, 20+30);
//    QLinearGradient linearGradient(QPoint(0, 0), QPoint(30, 30));
//    linearGradient.setColorAt(0.16 * 0, Qt::red              );
//    linearGradient.setColorAt(0.16 * 1, QColor(255,127,0,255));
//    linearGradient.setColorAt(0.16 * 2, Qt::yellow           );
//    linearGradient.setColorAt(0.16 * 3, Qt::green            );
//    linearGradient.setColorAt(0.16 * 4, QColor(0,255,255,255));
//    linearGradient.setColorAt(0.16 * 5, Qt::blue             );
//    linearGradient.setColorAt(0.16 * 6, QColor(139,0,255,255));

    _pain->setClipRegion(m_refresh.adjusted(-10,-10,10,10));
    if(m_click_status == T_Click_Refresh){
        _pain->setPen(QColor(0,0,0,0));
        _pain->setBrush(QColor(182, 206, 232, 255));
        _pain->drawRect(rect());
        _pain->translate(m_refresh.center());       //定义中心位置
    //    _pain->rotate(m_angle);                   //旋转角度

        int i_w = m_refresh.width();
        _pain->setBrush(QColor(245, 120, 220, 255));
        _pain->drawPie(QRect(-(i_w/2), -(i_w/2), i_w, i_w), -(1 * 16), -(m_angle * 16));
        _pain->setPen(QPen(Qt::white, 3));
        _pain->drawArc(QRect(-(i_w/2), -(i_w/2), i_w, i_w), -(1 * 16), -(m_angle * 16));
    //    _pain->drawText(QRect(-(i_w), -(i_w), i_w, i_w), "中");

    //    qDebug() << "<<<<<<<<<<< " << m_angle;
    }
    else{}
}

void BillWidget::paintTipText(QPainter *_pain)
{
    _pain->setPen(QColor(0, 0, 0 ,0));
    _pain->setBrush(m_color_cur_user);
    _pain->drawRect(m_cur_user);
    _pain->setPen(Qt::white);
    _pain->drawText(m_cur_user, Qt::AlignCenter, "当前缴费用户" );
}

void BillWidget::paintBill(QPainter * _pain)
{
    QString s_water, s_ele;
    QColor c_water, c_ele;
    getBill(s_water, s_ele, c_water, c_ele);

    _pain->setPen(QColor(0, 0, 0, 0));
    _pain->setBrush(c_water);
    _pain->drawRect(m_balance_water);
    _pain->setBrush(c_ele);
    _pain->drawRect(m_balance_electricity);
    _pain->setPen(Qt::white);

    int i_x, i_y, i_w, i_h;

    i_x = m_balance_water.x();
    i_y = m_balance_water.y();
    i_w = m_balance_water.width() / 2;
    i_h = m_balance_water.height();
    _pain->drawText(QRect(i_x      , i_y, i_w, i_h), Qt::AlignCenter, "water" );
    _pain->drawText(QRect(i_x + i_w, i_y, i_w, i_h), Qt::AlignCenter, s_water );

    i_x = m_balance_electricity.x();
    i_y = m_balance_electricity.y();
    i_w = m_balance_electricity.width() / 2;
    i_h = m_balance_electricity.height();
    _pain->drawText(QRect(i_x      , i_y, i_w, i_h), Qt::AlignCenter, "electricity" );
    _pain->drawText(QRect(i_x + i_w, i_y, i_w, i_h), Qt::AlignCenter, s_ele         );

}

void BillWidget::paintUser(QPainter *_pain)
{
    QString s_curr;
    QMap<QString, QString> map_user;
    getUser(map_user, s_curr);

    int i_x = m_user.x();
    int i_y = m_user.y();
    int i_w = m_user.width();
    int i_h = m_user.height();

    _pain->setPen(Qt::white);
    _pain->drawText(QRect(i_x, i_y - i_h, i_w, i_h), Qt::AlignCenter, "用户列表");

    auto begin = map_user.begin();
    for(int ifor=0; map_user.end() != begin; ifor++, begin++){
        QRect rect = QRect(i_x, i_y + (ifor * i_h), i_w, i_h);
        if(begin.key() == s_curr){
            _pain->setPen(QColor(0, 0, 0, 0));
            _pain->setBrush(m_color_cur_user);
            _pain->drawRect(rect);
            _pain->setPen(Qt::white);
            m_cur_user = rect;
        }
        _pain->drawText(rect, Qt::AlignCenter, begin.value());
    }

}

void BillWidget::paintEvent(QPaintEvent *_p)
{
    Q_UNUSED(_p);
    QPainter painter;
    painter.begin(this);
//    抗锯齿
    painter.setRenderHints(QPainter::Antialiasing | QPainter::TextAntialiasing | QPainter::SmoothPixmapTransform);

    QFont font;
    font.setBold(true);
    font.setFamily("Microsoft YaHei");
    font.setPointSize(20);
    painter.setFont(font);

    do{
        if(m_move_status != T_None){
            if(movePaint(&painter))  break;
        }
        if(m_click_status != T_None){
            if(clickPaint(&painter)) break;
        }

        //清空指定大小的绘画区
        painter.eraseRect(rect());
        //    背景色
        int i_w = rect().width() / 2;
        int i_h = rect().height() / 2;
        QRadialGradient radialGradient(QPointF(i_w, i_h), i_w, QPointF(i_w, i_h));
        radialGradient.setColorAt(0, QColor(245, 120, 220, 255));
        radialGradient.setColorAt(1, QColor(182, 206, 232, 255));
        painter.setBrush(radialGradient);
        painter.drawRect(rect());

    //    圆形刷新图标
//        QLinearGradient linearGradient(i_w, 20, i_w+30, 20+30);
//        linearGradient.setColorAt(0.16 * 0, Qt::red              );
//        linearGradient.setColorAt(0.16 * 1, QColor(255,127,0,255));
//        linearGradient.setColorAt(0.16 * 2, Qt::yellow           );
//        linearGradient.setColorAt(0.16 * 3, Qt::green            );
//        linearGradient.setColorAt(0.16 * 4, QColor(0,255,255,255));
//        linearGradient.setColorAt(0.16 * 5, Qt::blue             );
//        linearGradient.setColorAt(0.16 * 6, QColor(139,0,255,255));

        int i_s = 30;
        int i_x = i_w - i_s / 2;
        int i_y = (100 - i_s) / 2;
        m_refresh = QRect(i_x, i_y, i_s, i_s);
        painter.setPen(QPen(Qt::white, 5));
        painter.drawEllipse(m_refresh);
//        painter.drawArc(m_refresh, 1*16, 360*16);


//        painter.setClipRegion(m_refresh);

        //画圆环
//        painter.setPen(QColor(0,0,0,0));
//        painter.setBrush(Qt::white);
//        painter.drawEllipse(m_refresh);
//        painter.setBrush(QColor(182, 206, 232, 255));
//        painter.drawEllipse(m_refresh.adjusted(5,5,-5,-5));

        paintBill(&painter);
        paintUser(&painter);
    }while(false);

    painter.end();
}

void BillWidget::mousePressEvent(QMouseEvent *_move)
{
    QPoint p_pos = _move->pos();

    int i_x = p_pos.x();
    int i_y = p_pos.y();

    if(i_x > m_refresh.x() && i_y > m_refresh.y()){
        if(i_x - m_refresh.x() < m_refresh.width() && i_y - m_refresh.y() < m_refresh.height()){
            m_angle = 0;
            m_click_status = T_Click_Refresh;
            m_timer_process.start();
        }
    }
}

void BillWidget::mouseMoveEvent(QMouseEvent *_move)
{
    QPoint p_pos = _move->pos();

    int i_x = p_pos.x();
    int i_y = p_pos.y();

    if(i_x > m_cur_user.x() && i_y > m_cur_user.y()){
        if(i_x - m_cur_user.x() < m_cur_user.width() && i_y - m_cur_user.y() < m_cur_user.height()){
            if(T_None == (m_move_status | T_None)){
                m_move_status = T_Move_Curr;
                //重绘部分区域
                repaint(m_cur_user);
                m_move_status = T_Move_Curr | T_Complete;
            }
        }
        else    resetDrawWindow();
    }
    else    resetDrawWindow();
}

void BillWidget::s_timer_process()
{
    if(m_angle < 360){
        m_angle += 360/75;
        switch(m_click_status){
        case T_Click_Refresh:
            //        repaint();
            //        repaint(QRegion(m_refresh.adjusted(2,2,-3,-3), QRegion::Ellipse));
            //        repaint(QRegion(m_refresh.adjusted(-10,-10,10,10), QRegion::Ellipse));
            //        repaint(m_refresh);
            repaint(QRegion(m_refresh.adjusted(-10,-10,10,10), QRegion::Ellipse));
            break;
        default:
            m_angle = 0;
            m_timer_process.stop();
            return;
        }
    }
    else{
        m_click_status = T_None;
//        m_click_status = m_click_status | T_Complete;
        m_timer_process.stop();
//        m_timer_finish.start();
        repaint();
    }
}

void BillWidget::s_timer_finish()
{
    switch(m_click_status){
    case T_Click_Refresh | T_Complete:
        repaint(QRegion(m_refresh.adjusted(-10,-10,10,10), QRegion::Ellipse)); break;
    default:
        m_timer_finish.stop();
        m_click_status = T_None;
        return;
    }
}

