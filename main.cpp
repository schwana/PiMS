#include "quadctrl.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QuadCTRL w;
    w.show();

    return a.exec();
}
