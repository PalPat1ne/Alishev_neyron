#include <iostream>
#include <fstream>
#include <cmath>

using namespace std;

int main(int argn, char* argv[])
{
    float x1, x2, y, a0, a1, a2, v;
    int j;
    int num_inputs = 2;

    if (argn != 4)
        cerr << argv[0] << " in.txt coef.txt out.txt" << endl, exit(1);

    ifstream in(argv[2]);
    in >> a0 >> a1 >> a2;
    in.close();

    in.open(argv[1]);
    if (!in)
        cerr << "No read input file \"" << argv[1] << "\"" << endl, exit(2);

    for (j = 0;;)
        if (in >> y) j++;
        else break;

    in.close();

    int N = j / num_inputs;
    cout << "N=" << N << endl;

    ofstream out(argv[3]);

    in.open(argv[1]);
    for (j = 0; j < N; j++)
    {
        in >> x1 >> x2;

        v = a0 + a1 * x1 + a2 * x2;   /* модель нейрона */

        if (v > 0)
            y = 1;
        else
            y = 0;

        out << x1 << '\t' << x2 << '\t' << y << endl;
    }

    in.close();
    out.close();

    return 0;
}