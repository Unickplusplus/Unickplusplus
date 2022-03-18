
clock_t c_st, c_end;

double print_curTime(string prefix = "")
{
    c_end = clock();
    double totTime = (double)(c_end - c_st) / CLOCKS_PER_SEC;
    cout << prefix << "totalTime :" <<  totTime << endl;
    return totTime;
}
