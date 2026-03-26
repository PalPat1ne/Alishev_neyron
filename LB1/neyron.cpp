#include <iostream>
#include <fstream>
#include <cmath>
#include <string>
#include <cstdlib>

using namespace std;

float linear_activation(float v, float k, float b)
{
    return k * v + b;
}

float threshold_activation(float v)
{
    if (v < 0)
        return 0;

    return 1;
}

float sigmoid_activation(float v, float alpha)
{
    return 1.0f / (1.0f + exp(-alpha * v));
}

float bipolar_sigmoid_activation(float v, float alpha)
{
    return tanh(alpha * v);
}

int main(int argn, char* argv[])
{
    float x1, x2, y, a0, a1, a2, v;
    float alpha = 1.0f;
    float linear_k = 1.0f;
    float linear_b = 0.0f;
    int j;
    int num_inputs = 2;
    string mode = "2";

    if (argn < 4 || argn > 8)
        cerr << argv[0] << " in.txt coef.txt out.txt [activation] [alpha] [linear_k] [linear_b]" << endl, exit(1);

    if (argn >= 5)
        mode = argv[4];

    if (argn >= 6)
        alpha = atof(argv[5]);

    if (argn >= 7)
        linear_k = atof(argv[6]);

    if (argn >= 8)
        linear_b = atof(argv[7]);

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

        if (mode == "1" || mode == "linear")
            y = linear_activation(v, linear_k, linear_b);
        else if (mode == "2" || mode == "step" || mode == "threshold")
            y = threshold_activation(v);
        else if (mode == "3" || mode == "sigmoid")
            y = sigmoid_activation(v, alpha);
        else if (mode == "4" || mode == "tanh" || mode == "bipolar")
            y = bipolar_sigmoid_activation(v, alpha);
        else
            cerr << "Unknown activation: " << mode << endl, exit(3);

        out << x1 << '\t' << x2 << '\t' << y << endl;
    }

    in.close();
    out.close();

    return 0;
}
