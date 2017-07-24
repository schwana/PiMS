#ifndef DISPLAYSRS_H
#define DISPLAYSRS_H

#include <QMainWindow>

namespace Ui {
class displaySRS;
}

class displaySRS : public QMainWindow
{
    Q_OBJECT

public:
    explicit displaySRS(QWidget *parent = 0);
    ~displaySRS();

private:
    Ui::displaySRS *ui;
};

#endif // DISPLAYSRS_H
