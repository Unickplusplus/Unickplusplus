
//
//
//#include <stdio.h>
//#include <string.h>
//#include <map>
//#include <set>
//#include <vector>
//#include <iostream>
//#include <fstream>
//#include <sstream>
//#include <math.h>
//#include <stdlib.h>
//#include <time.h>
//#include <z3++.h>
//#include <unordered_set>
//#include <unordered_map>
//
//#include "checker.cpp"
//#include "support.cpp"
//
//using namespace std;
//#define MAX 100005
//#define MAX_ROUND 1000000
//
//bool arg_samples = false, arg_time = false;
//int max_samples = 10000000;
//double max_time = 7200.0, eps = 1e-6;
//
//
//int SAMPLE_ROUNDS = 100;
//
//int num_variable = 0, num_clause = 0, num_ind = 0, max_k = 0, max_d = 0;
//vector<set<int> > variables;
//vector<map<int, uint8_t> > clauses;
//set<int> ind_variables, ind_clauses;
//map<int, int> reverse_ind;
//vector<int> ind;
//ofstream result_file, expectation_file;
//
//
//unordered_set<string> initial_results;
//vector<string> initial_results_vec;
//
//inline double rand_double() { return (double) (rand() / (double) RAND_MAX);}
//
//
//
//void parse_cnf(string input_file)
//{
//    z3::expr_vector exp(c);
//    ifstream f(input_file);
//    if (!f.is_open())
//    {
//        std::cout << "Error opening input file\n";
//        abort();
//    }
//
//    string input_line;
//    int clause_cnt = 0;
//    while(getline(f, input_line))
//    {
//        istringstream iss(input_line);
//        if (input_line.find("c ind") == 0)
//        {
//            string temp_str;
//            int var = 0;
//
//            iss >> temp_str;
//            iss >> temp_str;
//            while(!iss.eof())
//            {
//                iss >> var;
//                if (var == 0) break;
//                ind_variables.insert(var);
//                ind.push_back(var);
//                reverse_ind[ind.size() - 1] = var;
//            }
//        }
//        else if(input_line[0] == 'p')
//        {
//            string temp_str;
//            iss >> temp_str;
//            iss >> temp_str;
//            iss >> num_variable >> num_clause;
//            for (int i = 0; i <= num_variable; i++)
//                variables.push_back(set<int>());
//            for (int i = 0; i <= num_clause; i++)
//                clauses.push_back(map<int, uint8_t>());
//        }
//        else
//        {
//            z3::expr_vector z3_clause(c);
//            clause_cnt = clause_cnt + 1;
//            int var = 0, var_abs = 0;
//            while(!iss.eof())
//            {
//                iss >> var;
//                if(var == 0) break;
//                var_abs = abs(var);
//                variables[var_abs].insert(clause_cnt);
//                clauses[clause_cnt].insert(pair<int, uint8_t>(var_abs, (var == var_abs) ? 1 : 0));
//                z3_clause.push_back(var == var_abs ? literal(var_abs) : !literal(var_abs));
//            }
//            if(!z3_clause.empty()) exp.push_back(z3::mk_or(z3_clause));
//        }
//        z3::expr z3_formula = z3::mk_and(exp);
//        opt.add(z3_formula);
//    }
//
//    num_ind = ind.size();
//
//    for (int i = 1; i <= num_variable; i++)
//        if (max_d < variables[i].size()) max_d = (int) variables[i].size();
//    for (int i = 1; i <= num_clause; i++)
//        if (max_k < clauses[i].size()) max_k = (int) clauses[i].size();
//}
//
//
//pair<double, double> approx_prob(string m_str, int index) // index in vector ind
//{
//    int var_name = ind[index];
//    set<int> target_clauses = variables[var_name];
//    double expectation[2] = {};
//    for(int target_clause : target_clauses)
//    {
//        map<int, uint8_t> target = clauses[target_clause];
//        int cnt_other = 0, flag = -1;
//        bool cnt_marked[2] = {};
//        for(auto & jt : target)
//        {
//            if(jt.first == var_name) flag = jt.second;
//            else if(ind_variables.find(jt.first) == ind_variables.end()) cnt_other++;
//            else
//            {
//                int cur_val = m_str[reverse_ind[jt.first]];
//                cnt_marked[jt.second == cur_val ? 1 : 0] = true;
//            }
//        }
//        if(cnt_marked[0]) expectation[0] += 1.0;
//        else if (flag == 0) expectation[0] += 1.0;
//        else expectation[0] += (1 - pow(0.5, cnt_other));
//
//        if(cnt_marked[1]) expectation[1] += 1.0;
//        else if (flag == 1) expectation[1] += 1.0;
//        else expectation[1] += (1 - pow(0.5, cnt_other));
//    }
//    double exp_sum = expectation[0] + expectation[1];
//
////    if(exp_sum < eps) expectation_file << 0 << ' ' << 0 << endl;
////    else expectation_file << expectation[0] << ' ' << expectation[1]  << endl;
//
//    return exp_sum < eps ? pair<double, double>(0.5, 0.5) : pair<double, double>(expectation[0] / exp_sum,expectation[1] / exp_sum);
//}
//
//string prob_mutate(string input_str, int index, pair<double, double> prob)
//{
//    if (rand_double() < prob.first) input_str[index] = '0';
//    else input_str[index] = '1';
//    return input_str;
//}
//
//string model_string(z3::model & model) {
//    string res;
//
//    for (int v : ind)
//    {
//        z3::func_decl decl(literal(v).decl());
//        z3::expr b = model.get_const_interp(decl);
//        if (b.bool_value() == Z3_L_TRUE) res += "1";
//        else res += "0";
//    }
//    return res;
//}
//
//
//
//
//string mcmc_sample(string init_str)
//{
//    for(int i = 0; i < SAMPLE_ROUNDS; i++)
//    {
//        int index = abs(rand()) % num_ind;
//        pair<double, double> distribution = approx_prob(init_str, index);
//        init_str = prob_mutate(init_str, index, distribution);
//    }
//    return init_str;
//}
//
//int legal_count[2] = {};
//
//void run()
//{
//    SAMPLE_ROUNDS = num_ind;
////    SAMPLE_ROUNDS = 10;
//    print_curTime();
//    while(true)
//    {
//        opt.push();
//        for(int v : ind_variables)
//        {
//            opt.add(rand() % 2 ? literal(v) : !literal(v), 1);
//        }
//        if (!solve())
//        {
//            cout << "Could not find a solution!\n";
//            exit(0);
//        }
//        z3::model z3_model = opt.get_model();
//        opt.pop();
//
//        string m_string = model_string(z3_model);
//        initial_results.clear();
//        initial_results_vec.clear();
//        initial_results.insert(m_string);
//        initial_results_vec.push_back(m_string);
//
//
//        cout << m_string << endl;
//
//        print_curTime();
//
//        for(int i = 0; i < 100; i++)
//        {
//            string mcmc_res = mcmc_sample(m_string);
//            bool satisfied = check_inds(mcmc_res, ind, num_variable);
//            if (satisfied) legal_count[1]++;
//            else legal_count[0]++;
//            result_file << mcmc_res << endl;
//        }
////        opt.push();
//
//        double curTime = print_curTime();
//
//        if (curTime > 10) break;
//  }
//}
//
//void curious(int rounds)
//{
//    int res[2] = {};
//    for(int i = 0; i < rounds; i++)
//    {
//        string temp = "";
//        for(int ind: ind)
//        {
//            temp += (rand() % 2 ?  "0" : "1");
//        }
//        bool legal = check_inds(temp, ind);
//        if(legal) res[1]++;
//        else res[0]++;
//
//        if(i % 10 == 0)
//        {
//            printf("temp_curious : %d\n", i);
//            printf("curious: %d %d\n", res[0], res[1]);
//        }
//    }
//}
//
//int main(int argc, char *argv[])
//{
//    if (argc < 2)
//    {
//        cout << "Argument required: input file\n";
////        helpMsg();
//        abort();
//    }
//
//    for (int i = 1; i < argc; ++i)
//    {
//        if (strcmp(argv[i], "-n") == 0) arg_samples = true;
//        else if (strcmp(argv[i], "-t") == 0) arg_time = true;
//        else if (arg_samples)
//        {
//            arg_samples = false;
//            max_samples = atoi(argv[i]);
//        }
//        else if (arg_time)
//        {
//            arg_time = false;
//            max_time = atof(argv[i]);
//        }
//    }
//
//    parse_cnf(string(argv[argc - 1]));
//    result_file.open(string(argv[argc - 1]) + ".mcmc_samples");
//    expectation_file.open("../statistics/expectation.txt");
//
//    srand((unsigned int) time(NULL));
//
//    printf("%lu %lu\n", variables.size(), clauses.size());
//    printf("K : %d, D : %d\n", max_k, max_d);
//
//    c_st = clock();
//
////    curious(1000);
//
//    run();
//    printf("legal: %d %d\n", legal_count[0], legal_count[1]);
////    partial_reject();
//    result_file.close();
//    expectation_file.close();
//
//    c_end = clock();
//    double totTime = (double)(c_end - c_st) / CLOCKS_PER_SEC;
//    printf("Tot time : %lf\n", totTime);
//}
//
//
//
//
//
//bool partial_reject()
//{
//
//    int rounds = 0;
//    vector<int> resamples(num_variable + 1);
//    vector<uint8_t> input(num_variable + 1);
//    for (int i = 0; i <= num_variable; i++) input[i] = uint8_t(rand() & 0x1);
//    while(++rounds < MAX_ROUND)
//    {
//        set<int> violation;
//        for (int i = 1; i <= num_clause; i++)
//        {
//            map<int, uint8_t>::iterator it;
//            bool legal = false;
//            for (it = clauses[i].begin(); it != clauses[i].end(); it++)
//            {
//                if (input[it -> first] == it -> second)
//                {
//                    legal = true;
//                    break;
//                }
//            }
//            if (!legal)
//            {
//                for (it = clauses[i].begin(); it != clauses[i].end(); it++)
//                {
//                    violation.insert(it -> first);
//                    resamples[it -> first]++;
//                }
//            }
//        }
//        if (violation.size() == 0)
//        {
//            printf("SUCCESS ROUNDS : %d\n", rounds);
//            return true;
//        }
//        printf("Violation : %lu\n", violation.size());
//        set<int>::iterator it;
//        for(it = violation.begin(); it != violation.end(); it++)
//        {
//            input[*it] = uint8_t(rand() & 0x1);
//        }
//    }
//    printf("Fail!\n");
//    for (int i = 1; i <= num_variable; i++) printf("%d : %d\n", i, resamples[i]);
//    return false;
//}
//





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
    int single_round = num_ind;
    if (single_round > 400) single_round = 400;
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

            t3 = print_curTime();
            bool satisfied = check_inds(quick_res, ind);
            if (satisfied) legal_count[1]++;
            else legal_count[0]++;
            t4 = print_curTime();
            temp_time = temp_time + (t4 - t3);
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
    bool use_list = false;

    string m_string;
    while(true)
    {
        if(waiting.empty())
        {
            use_list = false;
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
//            cout << "new point\n";

            for(int i = 0; i < 6; i++)
            {
                int index = rand() % num_ind;
                string last = m_string;
                if (!waiting.empty()) last = waiting.back();
                if(last[i] == '1') opt.add(!literal(ind[index]));
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
            use_list = true;
            m_string = waiting.front();
        }

//        legal_count[1]++;
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
//            cout << quick_res << endl;
//            printf("legal: %d %d\n", legal_count[0], legal_count[1]);
            result_file << "1: " + quick_res << endl;
        }
        if(use_list) waiting.pop_front();

        t2 = print_curTime();
        sum_time = sum_time + (t2 - t1);

        max_number = max_number - single_round;
        if(max_number < 0)
        {
            real_number = real_number - max_number;
            break;
        }

//        double curTime = print_curTime();
//
//        if (curTime > max_time) break;
    }
}

int max_samples = 2000, max_time = 120;



void gen(int argc, char *argv[])
{
    parse_cnf(string(argv[argc - 2]));
    result_file.open(string(argv[argc - 1]));
//    log_file.open("../theory/time/brute.json", ofstream::app);

    //    expectation_file.open("../statistics/expectation.txt");
    cout << "lll\n";
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
    log_file.open("../theory/time/mcmc-implement.json", ofstream::app);
    log_file << R"(, { "name" : ")" + string(argv[argc - 3]) + R"(", "num" : )"  << real_number << + ", \"sumTime\" : " << sum_time
             << ", \"illegal\" : " << legal_count[0] << ", \"legal\" : " << legal_count[1] << ", \"tempTime\" : " << temp_time << "}";
    log_file.close();

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
    gen(argc, argv);

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









