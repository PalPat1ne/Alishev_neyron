#include <iostream>
#include <fstream>
#include <cmath>

using namespace std;

int main(int argn, char* argv[])
{
    int i, j, k, t, N;
    float delta = 0.1;          // step
    float L = 1;                // input signal -L...L with step delta
    int num_inputs = 2;

    if (argn != 2)
        cerr << argv[0] << " sig.txt" << endl, exit(1);

    cout << "num_inputs=" << num_inputs << endl;

    k = 1 + 2 * L / delta + 1e-6;   // steps
    cout << "k=" << k << endl;

    t = 1 + log10(1 / delta + 1e-6);   // precision
    cout << "t=" << t << endl;

    for (N = j = 1; j <= num_inputs; j++)
        N *= k;

    cout << "N=" << N << endl;

    if (N < 1)
        cerr << "Error: N<1!" << endl, exit(1);

    float* X = new float[num_inputs];

    for (i = 0; i < num_inputs; i++)
        X[i] = -L;

    for (i = 0; i < num_inputs; i++)
        cout << X[i] << '\t';

    cout << endl;

    cout << "argv[1]=" << argv[1] << endl;

    ofstream out(argv[1]);

    if (!out)
        cerr << "No create output file \"" << argv[1] << "\"" << endl, exit(2);

    out.precision(t);

    for (j = 0; j < N; j++)
    {
        for (i = 0; i < num_inputs; out << X[i++] << '\t');

        out << endl;

        for (k = 0; k < num_inputs; k++)
            if (X[k] > L - 1e-6)
                X[k] = -L;
            else
            {
                X[k] += delta;
                break;
            }

        if (fabs(X[k]) < 1e-6)
            X[k] = 0;
    }

    out.close();
    delete[] X;

    return 0;
}