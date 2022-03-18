
#include <stdio.h>
#include <string.h>
#include <map>
#include <set>
#include <vector>
#include <deque>
#include <iostream>
#include <fstream>
#include <sstream>
#include <math.h>
#include <stdlib.h>
#include <time.h>
#include <z3++.h>
#include <unordered_set>


using namespace std;

bool arg_samples = false, arg_time = false;

clock_t c_st, c_end;

double print_curTime(string prefix = "")
{
    c_end = clock();
    double totTime = (double)(c_end - c_st) / CLOCKS_PER_SEC;
//    cout << prefix << "totalTime :" <<  totTime << endl;
    return totTime;
}



int SAMPLE_ROUNDS = 100;

int num_variable = 0, num_clause = 0, num_ind = 0;
vector<int> ind;
ofstream result_file, log_file;


z3::context c;
z3::optimize opt(c);


z3::expr literal(int v)
{
    return c.constant(c.str_symbol(std::to_string(v).c_str()), c.bool_sort());
}

void parse_cnf(string input_file)
{
    z3::expr_vector exp(c);
    std::ifstream f(input_file);
    if (!f.is_open()) {
        std::cout << "Error opening input file\n";
        abort();
    }
    unordered_set<int> indset;
    bool has_ind = false;
    int max_var = 0;
    std::string line;
    while (getline(f, line)) {
        std::istringstream iss(line);
        if(line.find("c ind ") == 0) {
            std::string s;
            iss >> s;
            iss >> s;
            int v;
            while (!iss.eof()) {
                iss >> v;
                if (v && indset.find(v) == indset.end()) {
                    indset.insert(v);
                    ind.push_back(v);
                    has_ind = true;
                }
            }
        } else if (line[0] != 'c' && line[0] != 'p') {
            z3::expr_vector clause(c);
            int v;
            while (!iss.eof()) {
                iss >> v;
                if (v > 0)
                    clause.push_back(literal(v));
                else if (v < 0)
                    clause.push_back(!literal(-v));
                v = abs(v);
                if (!has_ind && v != 0)
                    indset.insert(v);
                if (v > max_var)
                    max_var = v;
            }
            if (clause.size() > 0)
                exp.push_back(mk_or(clause));
        }
    }
    f.close();
    if (!has_ind) {
        for (int lit = 0; lit <= max_var; ++lit) {
            if (indset.find(lit) != indset.end()) {
                ind.push_back(lit);
            }
        }
    }
    z3::expr formula = mk_and(exp);
    opt.add(formula);
    num_ind = ind.size();
}


string model_string(z3::model & model) {
    string res;

    for (int v : ind)
    {
        z3::func_decl decl(literal(v).decl());
        z3::expr b = model.get_const_interp(decl);
        if (b.bool_value() == Z3_L_TRUE) res += "1";
        else res += "0";
    }
    return res;
}

bool solve()
{
    z3::check_result result = opt.check();
    return result == z3::sat;
}

bool check_inds(string m_str, vector<int> & ind)
{
    opt.push();
    int num_ind = ind.size();
    for(int i = 0; i < num_ind; i++)
    {
        int v = ind[i];
        opt.add( m_str[i] == '1' ? literal(v) : !literal(v));
    }
    bool res = solve();

    opt.pop();
    return res;
}

int legal_count[2] = {};
double sum_time = 0, temp_time = 0;

//string quick_shuffle(string init_str)
//{
//    for(int i = 0; i < SAMPLE_ROUNDS; i++)
//    {
//        int index = abs(rand()) & num_ind;
//        init_str[index] = init_str[index] == '1' ? '0' : '1';
//    }
//    return init_str;
//}

int real_number = 0;


void run_brute(int max_number, int max_time)
{
//    SAMPLE_ROUNDS = num_ind;
    real_number = max_number;
    SAMPLE_ROUNDS = 2;
    print_curTime();

    double t1, t2, t3, t4;
    int single_round = num_ind * num_ind;
    if (single_round > (int) sqrt(40)) single_round = (int) sqrt(40);
    if (single_round < 2) single_round = 2;

    while(true)
    {
        opt.push();
        for(int v : ind)
        {
            opt.add(rand() % 2 ? literal(v) : !literal(v), 1);
        }

        t1 = print_curTime();
        if (!solve())
        {
            cout << "Could not find a solution!\n";
            exit(0);
        }
        t2 = print_curTime();
        sum_time = sum_time + (t2 - t1);

        z3::model z3_model = opt.get_model();
        opt.pop();

        string m_string = model_string(z3_model);
        result_file <<  "0: " + m_string << endl;

//        cout << "0: " + m_string << endl;

        t1 = print_curTime();
        for(int cnt = 0; cnt < single_round; cnt++)
        {
            int index;
            string quick_res = m_string;
            index = rand() % num_ind;
            quick_res[index] = quick_res[index] == '1' ? '0' : '1';
            index = rand() % num_ind;
            quick_res[index] = quick_res[index] == '1' ? '0' : '1';

//            cout << quick_res << endl;
//            printf("legal: %d %d\n", legal_count[0], legal_count[1]);
            result_file << "1: " + quick_res << endl;
        }
        t2 = print_curTime();
        sum_time = sum_time + (t2 - t1);

        max_number = max_number - single_round;
        if(max_number < 0)
        {
            real_number = real_number - max_number;
            break;
        }
/*
//        print_curTime();
        int max_ind = (int) pow(num_ind, SAMPLE_ROUNDS);
        if(max_ind > max_number) max_ind = max_number;
        for(int cnt = 1; cnt < max_ind; cnt++)
        {
            int temp = cnt, index = 0;
            string quick_res = m_string;
            for(int i = 0; i < SAMPLE_ROUNDS; i++)
            {
                index = temp % num_ind;
                quick_res[index] = quick_res[index] == '1' ? '0' : '1';
                temp = temp / num_ind;
            }
//            bool satisfied = check_inds(quick_res, ind);
//            if (satisfied) legal_count[1]++;
//            else legal_count[0]++;
//            cout << quick_res << endl;
//            printf("legal: %d %d\n", legal_count[0], legal_count[1]);
            result_file << quick_res << endl;
        }


//        for(int cnt = 1; cnt < num_ind; cnt++)
//        {
//            string quick_res = m_string;
//            int index = cnt % num_ind;
//            quick_res[index] = quick_res[index] == '1' ? '0' : '1';
//
//            bool satisfied = check_inds(quick_res, ind);
//            if (satisfied) legal_count[1]++;
//            else legal_count[0]++;
//            cout << quick_res << endl;
//            printf("legal: %d %d\n", legal_count[0], legal_count[1]);
//            result_file << quick_res << endl;
//        }
*/

//        double curTime = print_curTime();
//
//        if (curTime > max_time) break;
    }
}



void run(int max_number, int max_time)
{
//    SAMPLE_ROUNDS = num_ind;
    real_number = max_number;
    SAMPLE_ROUNDS = 2;
    print_curTime();

    double t1, t2, t3, t4;
    int single_round = num_ind;
    if (single_round > 400) single_round = 400;
    if (single_round < 2) single_round = 2;

    deque<string> waiting;
    int step = -1;

    string m_string;
    while(true)
    {
        if(waiting.empty())
        {
            opt.push();
            for (int v: ind) {
                opt.add(rand() % 2 ? literal(v) : !literal(v), 1);
            }

            t1 = print_curTime();
            if (!solve()) {
                cout << "Could not find a solution!\n";
                exit(0);
            }
            t2 = print_curTime();
            sum_time = sum_time + (t2 - t1);

            z3::model z3_model = opt.get_model();

            m_string = model_string(z3_model);

            for(int i = 0; i < 6; i++)
            {
                int index = rand() % num_ind;
                if(waiting.back()[i] == '1') opt.add(!literal(ind[index]));
                else opt.add(literal(ind[index]));
                if(solve())
                {
                    z3::model new_model = opt.get_model();
                    waiting.push_back(model_string(new_model));
                }
                else
                {
                    break;
                }
            }

            opt.pop();
        }
        else
        {
            m_string = waiting.front();
        }

        result_file <<  "0: " + m_string << endl;

//        cout << "0: " + m_string << endl;

        t1 = print_curTime();
        for(int cnt = 0; cnt < single_round; cnt++)
        {
            int index;
            string quick_res = m_string;
            index = rand() % num_ind;
            quick_res[index] = quick_res[index] == '1' ? '0' : '1';

            t3 = print_curTime();
            bool satisfied = check_inds(quick_res, ind);
            if (satisfied) legal_count[1]++;
            else legal_count[0]++;
            t4 = print_curTime();
            temp_time = temp_time + (t4 - t3);
            cout << quick_res << endl;
            printf("legal: %d %d\n", legal_count[0], legal_count[1]);
            result_file << "1: " + quick_res << endl;
        }
        waiting.pop_front();

        t2 = print_curTime();
        sum_time = sum_time + (t2 - t1);

        max_number = max_number - single_round;
        if(max_number < 0)
        {
            real_number = real_number - max_number;
            break;
        }
/*
//        print_curTime();
        int max_ind = (int) pow(num_ind, SAMPLE_ROUNDS);
        if(max_ind > max_number) max_ind = max_number;
        for(int cnt = 1; cnt < max_ind; cnt++)
        {
            int temp = cnt, index = 0;
            string quick_res = m_string;
            for(int i = 0; i < SAMPLE_ROUNDS; i++)
            {
                index = temp % num_ind;
                quick_res[index] = quick_res[index] == '1' ? '0' : '1';
                temp = temp / num_ind;
            }
//            bool satisfied = check_inds(quick_res, ind);
//            if (satisfied) legal_count[1]++;
//            else legal_count[0]++;
//            cout << quick_res << endl;
//            printf("legal: %d %d\n", legal_count[0], legal_count[1]);
            result_file << quick_res << endl;
        }


//        for(int cnt = 1; cnt < num_ind; cnt++)
//        {
//            string quick_res = m_string;
//            int index = cnt % num_ind;
//            quick_res[index] = quick_res[index] == '1' ? '0' : '1';
//
//            bool satisfied = check_inds(quick_res, ind);
//            if (satisfied) legal_count[1]++;
//            else legal_count[0]++;
//            cout << quick_res << endl;
//            printf("legal: %d %d\n", legal_count[0], legal_count[1]);
//            result_file << quick_res << endl;
//        }
*/

//        double curTime = print_curTime();
//
//        if (curTime > max_time) break;
    }
}

void quicksampler_test(string input_res)
{
    std::ifstream f(input_res);
    if (!f.is_open()) {
        std::cout << "Error opening input file\n";
        abort();
    }
    string l, r;
    while(f >> l >> r)
    {
        bool satisfied = check_inds(r, ind);
        if (satisfied) legal_count[1]++;
        else legal_count[0]++;
    }

}

void ssampler_test(string input_res)
{
    std::ifstream f(input_res);
    if (!f.is_open()) {
        std::cout << "Error opening input file\n";
        abort();
    }
    string r;
//    int legal[2] = {};
    while(f >> r)
    {
        bool satisfied = check_inds(r, ind);
        if (satisfied) legal_count[1]++;
        else legal_count[0]++;
//        cout << r << endl;
//        printf("legal: %d %d\n", legal[0], legal[1]);
    }

}

int max_samples = 2000, max_time = 120;


void test(int argc, char *argv[])
{
//    cout << "wow" << argv[argc - 2] << endl;
    parse_cnf(string(argv[argc - 2]));

    srand((unsigned int) time(NULL));

    c_st = clock();

    quicksampler_test(string(argv[argc - 1]));

    printf("legal: %d %d\n", legal_count[0], legal_count[1]);

    c_end = clock();
    double totTime = (double)(c_end - c_st) / CLOCKS_PER_SEC;
    printf("Tot time : %lf\n", totTime);

    log_file.open("../theory/time/quick-check.json", ofstream::app);
    log_file << R"(, { "name" : ")" + string(argv[argc - 3]) + R"(", "num" : )"  << real_number << + ", \"sumTime\" : " << totTime
             << ", \"illegal\" : " << legal_count[0] << ", \"legal\" : " << legal_count[1] << ", \"tempTime\" : " << temp_time << "}";
    log_file.close();

}

void gen_old(int argc, char *argv[])
{
    parse_cnf(string(argv[argc - 2]));
    result_file.open(string(argv[argc - 1]));
//    log_file.open("../theory/time/brute.json", ofstream::app);

    //    expectation_file.open("../statistics/expectation.txt");

    srand((unsigned int) time(NULL));

//    printf("%lu %lu\n", variables.size(), clauses.size());
//    printf("K : %d, D : %d\n", max_k, max_d);

    c_st = clock();

//    quicksampler_test(string(argv[argc - 1]) + ".samples");
    run(max_samples, max_time);

    printf("legal: %d %d\n", legal_count[0], legal_count[1]);
    result_file.close();
//    expectation_file.close();

    c_end = clock();
    log_file.open("../theory/time/brute.json", ofstream::app);
    log_file << ", " + string(argv[argc - 2]) + " : " << sum_time;
    log_file.close();

    double totTime = (double)(c_end - c_st) / CLOCKS_PER_SEC;
    printf("Tot time : %lf\n", sum_time);

}


void gen_brute(int argc, char *argv[])
{
    parse_cnf(string(argv[argc - 2]));
    result_file.open(string(argv[argc - 1]));
//    log_file.open("../theory/time/brute.json", ofstream::app);

    //    expectation_file.open("../statistics/expectation.txt");

    srand((unsigned int) time(NULL));

//    printf("%lu %lu\n", variables.size(), clauses.size());
//    printf("K : %d, D : %d\n", max_k, max_d);

    c_st = clock();

//    quicksampler_test(string(argv[argc - 1]) + ".samples");
    run_brute(max_samples, max_time);

    printf("legal: %d %d\n", legal_count[0], legal_count[1]);
    result_file.close();
//    expectation_file.close();

    c_end = clock();
    log_file.open("../theory/time/brute.json", ofstream::app);
    log_file << R"(, { "name" : ")" + string(argv[argc - 3]) + R"(", "num" : )"  << real_number << + ", \"sumTime\" : " << sum_time
             << ", \"illegal\" : " << legal_count[0] << ", \"legal\" : " << legal_count[1] << ", \"tempTime\" : " << temp_time << "}";
    log_file.close();

    double totTime = (double)(c_end - c_st) / CLOCKS_PER_SEC;
    printf("Tot time : %lf\n", sum_time);

}

void gen(int argc, char *argv[])
{
    parse_cnf(string(argv[argc - 2]));
    result_file.open(string(argv[argc - 1]));
//    log_file.open("../theory/time/brute.json", ofstream::app);

    //    expectation_file.open("../statistics/expectation.txt");

    srand((unsigned int) time(NULL));

//    printf("%lu %lu\n", variables.size(), clauses.size());
//    printf("K : %d, D : %d\n", max_k, max_d);

    c_st = clock();

//    quicksampler_test(string(argv[argc - 1]) + ".samples");
    run(max_samples, max_time);

    printf("legal: %d %d\n", legal_count[0], legal_count[1]);
    result_file.close();
//    expectation_file.close();

    c_end = clock();
    log_file.open("../theory/time/brute.json", ofstream::app);
    log_file << R"(, { "name" : ")" + string(argv[argc - 3]) + R"(", "num" : )"  << real_number << + ", \"sumTime\" : " << sum_time
    << ", \"illegal\" : " << legal_count[0] << ", \"legal\" : " << legal_count[1] << ", \"tempTime\" : " << temp_time << "}";
    log_file.close();

    double totTime = (double)(c_end - c_st) / CLOCKS_PER_SEC;
    printf("Tot time : %lf\n", sum_time);

}

void gen_without_log(int argc, char *argv[])
{
    parse_cnf(string(argv[argc - 2]));
    result_file.open(string(argv[argc - 1]));
//    log_file.open("../theory/time/brute.json", ofstream::app);

    //    expectation_file.open("../statistics/expectation.txt");

    srand((unsigned int) time(NULL));

//    printf("%lu %lu\n", variables.size(), clauses.size());
//    printf("K : %d, D : %d\n", max_k, max_d);

    c_st = clock();

//    quicksampler_test(string(argv[argc - 1]) + ".samples");
    run_brute(max_samples, max_time);

    printf("legal: %d %d\n", legal_count[0], legal_count[1]);
    result_file.close();
//    expectation_file.close();

    c_end = clock();

    double totTime = (double)(c_end - c_st) / CLOCKS_PER_SEC;
    printf("Tot time : %lf\n", sum_time);

}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        cout << "Argument required: input file\n";
//        helpMsg();
        abort();
    }

    for (int i = 1; i < argc; ++i)
    {
        if (strcmp(argv[i], "-n") == 0) arg_samples = true;
        else if (strcmp(argv[i], "-t") == 0) arg_time = true;
        else if (arg_samples)
        {
            arg_samples = false;
            max_samples = atoi(argv[i]);
        }
        else if (arg_time)
        {
            arg_time = false;
            max_time = atof(argv[i]);
        }
    }
//    test(argc, argv);
    gen_without_log(argc, argv);

//    parse_cnf(string(argv[argc - 2]));
//    result_file.open(string(argv[argc - 1]));
////    expectation_file.open("../statistics/expectation.txt");
//
//    srand((unsigned int) time(NULL));
//
////    printf("%lu %lu\n", variables.size(), clauses.size());
////    printf("K : %d, D : %d\n", max_k, max_d);
//
//    c_st = clock();
//
//    ssampler_test(string(argv[argc - 1]) + ".samples");
////    quicksampler_test(string(argv[argc - 1]) + ".samples");
////    run(max_samples, max_time);
//
//    printf("legal: %d %d\n", legal_count[0], legal_count[1]);
//    result_file.close();
////    expectation_file.close();
//
//    c_end = clock();
//    double totTime = (double)(c_end - c_st) / CLOCKS_PER_SEC;
//    printf("Tot time : %lf\n", totTime);
}









