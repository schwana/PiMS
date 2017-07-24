#include "displaysrs.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    displaySRS w;
    w.show();

    return a.exec();
}
