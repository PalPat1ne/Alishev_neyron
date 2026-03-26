#include <iostream>
#include <fstream>
#include <ctime>
#include <cmath>
float f(float x) { return tanh(x); }
float noise(float s)
{
    long long r;
    int i;
    for (r = -(RAND_MAX + 1LL) * 6, i = 0; i < 12; i++)
        r += rand();
    s *= r / (RAND_MAX + 1.);
    return s;
}
using namespace std;
int main(int argn, char *argv[])
{
    int i, k, K, N;
    float s0, sL, y0, yL, t, gamma = 0.1, sigma = 0, e2 = 0, min_eps = 0;
    const float eps_limit = 0.1f;
    if (argn != 5 && argn != 6)
        cerr << argv[0] << " coef.txt Niter gamma sigma [eps_history.txt]" << endl, exit(1);
    ifstream in(argv[1]);
    if (!in)
        cerr << "No read input file \"" << argv[1] << "\"" << endl, exit(2);
    for (K = 0;;)
        if (in >> s0)
            K++;
        else
            break; // Number coef
    in.close();
    N = atoi(argv[2]);
    cout << "N=" << N << endl;
    if (N < 1)
        cerr << "Error N<1!" << endl, exit(1);
    gamma = atof(argv[3]);
    cout << "gamma=" << gamma << endl;
    if (gamma <= 0)
        cerr << "Error gamma<=0!" << endl, exit(1);
    sigma = atof(argv[4]);
    cout << "sigma=" << sigma << endl;
    if (sigma < 0)
        cerr << "Error sigma<0!" << endl, exit(1);
    float *w0 = new float[K]; // Mass ves coef orig
    float *wL = new float[K]; // Mass ves coef learning
    in.open(argv[1]);
    srand(time(NULL));
    for (i = -1; ++i < K; in >> w0[i], wL[i] = 0)
        ;
    in.close();
    float *x = new float[K]; // Mass input signal
    ofstream out;
    if (argn == 6)
        out.open(argv[5]);
    for (i = -1; ++i < K;)
        cout << "w0[" << i << "]=" << w0[i] << endl;
    int success_step = -1;
    for (e2 = 0, i = -1; ++i < K;)
        e2 += (w0[i] - wL[i]) * (w0[i] - wL[i]);
    min_eps = e2;
    if (argn == 6)
        out << 0 << '\t' << e2 << endl;
    for (k = -1; ++k < N;)
    {
        for (i = -1; ++i < K;)
            x[i] = 1 - 2 * (rand() % 2) + noise(sigma);
        for (s0 = sL = 0, i = -1; ++i < K;)
            s0 += x[i] * w0[i];
        y0 = f(s0);
        for (sL = 0, i = -1; ++i < K;)
            sL += x[i] * wL[i];
        yL = f(sL);
        t = y0 - yL;
        for (i = 0; i < K; i++)
            wL[i] += gamma * x[i] * t;
        for (e2 = 0, i = -1; ++i < K;)
            e2 += (w0[i] - wL[i]) * (w0[i] - wL[i]);
        if (e2 < min_eps)
            min_eps = e2;
        if (argn == 6)
            out << k + 1 << '\t' << e2 << endl;
        if (success_step < 0 && e2 < eps_limit)
            success_step = k + 1;
    }
    cout << "y0-yL=" << t << endl;
    for (i = -1; ++i < K;)
        cout << "w0[" << i << "]=" << w0[i] << endl;
    for (i = -1; ++i < K;)
        cout << "wL[" << i << "]=" << wL[i] << endl;
    cout << "||w0-wL||^2=" << e2 << endl;
    cout << "min_eps2=" << min_eps << endl;
    if (success_step >= 0)
        cout << "first_success_step=" << success_step << endl;
    else
        cout << "first_success_step=not_found" << endl;
    if (argn == 6)
        out.close();
    delete[] x;
    delete[] wL;
    delete[] w0;
    return 0;
}
