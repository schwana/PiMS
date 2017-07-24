#ifndef QUADCTRL_H
#define QUADCTRL_H

#include <QMainWindow>

namespace Ui {
class QuadCTRL;
}

class QuadCTRL : public QMainWindow
{
    Q_OBJECT

public:
    explicit QuadCTRL(QWidget *parent = 0);
    ~QuadCTRL();

private:
    Ui::QuadCTRL *ui;
};

#endif // QUADCTRL_H
