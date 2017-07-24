#include "displaysrs.h"
#include "ui_displaysrs.h"

displaySRS::displaySRS(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::displaySRS)
{
    ui->setupUi(this);
}

displaySRS::~displaySRS()
{
    delete ui;
}
