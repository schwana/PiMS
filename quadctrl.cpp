#include "quadctrl.h"
#include "ui_quadctrl.h"

QuadCTRL::QuadCTRL(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::QuadCTRL)
{
    ui->setupUi(this);
}

QuadCTRL::~QuadCTRL()
{
    delete ui;
}
