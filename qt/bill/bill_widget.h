#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
#include <QTimer>

enum Mouse_Type{
    T_None,          //第一次画 0
    T_Complete,      //已画过   1
    T_Move_Curr,
    T_Move_Refresh      = T_Move_Curr    + 2,
    T_Click_Refresh     = T_Move_Refresh + 2
};

class BillWidget : public QWidget
{
    Q_OBJECT

public:
    BillWidget(QWidget *parent = nullptr);
    ~BillWidget();

private:
    QRect m_user;
    QRect m_cur_user;
    QRect m_balance_water;
    QRect m_balance_electricity;
    QRect m_refresh;

    QColor m_color_tall;
    QColor m_color_centre;
    QColor m_color_low;
    QColor m_color_cur_user;

    QTimer m_timer_process;
    QTimer m_timer_finish;

    unsigned int m_angle;
    unsigned int m_move_status;
    unsigned int m_click_status;

private:
    void getColor(int _val, QColor &_color);
    void getBill(QString &_water, QString &_ele, QColor &_c_water, QColor &_c_ele);
    void getUser(QMap<QString, QString> &_l_user, QString &_curr);
    void setConfig();
    void resetDrawWindow();

    bool movePaint(QPainter * _pain);
    bool clickPaint(QPainter * _pain);

    void paintRound(QPainter * _pain);
    void paintTipText(QPainter * _pain);
    void paintBill(QPainter * _pain);
    void paintUser(QPainter * _pain);
protected:
    void paintEvent(QPaintEvent *_p) override;
    void mousePressEvent(QMouseEvent *_move) override;
    void mouseMoveEvent(QMouseEvent *_move) override;

private slots:
    void s_timer_process();
    void s_timer_finish();

};
#endif // WIDGET_H
