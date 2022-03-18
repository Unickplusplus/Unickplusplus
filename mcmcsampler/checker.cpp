
#include <stdio.h>
#include <string.h>
#include <map>
#include <set>
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include <math.h>
#include <stdlib.h>
#include <time.h>
#include <z3++.h>
#include <unordered_set>
#include <unordered_map>
using namespace std;




z3::context c;
z3::optimize opt(c);


z3::expr literal(int v)
{
    return c.constant(c.str_symbol(std::to_string(v).c_str()), c.bool_sort());
}


bool solve() {
//    struct timespec start;
//    clock_gettime(CLOCK_REALTIME, &start);
//    double elapsed = duration(&start_time, &start);
//    if (elapsed > max_time) {
//        std::cout << "Stopping: timeout\n";
//        finish();
//    }
//    if (samples >= max_samples) {
//        std::cout << "Stopping: samples\n";
//        finish();
//    }

    z3::check_result result = opt.check();
//    struct timespec end;
//    clock_gettime(CLOCK_REALTIME, &end);
//    solver_time += duration(&start, &end);
//    solver_calls += 1;

    return result == z3::sat;
}


bool check_inds(string m_str, vector<int> & ind, int num_variable = 0)
{
    opt.push();
    int num_ind = ind.size();
    for(int i = 0; i < num_ind; i++)
    {
        int v = ind[i];
        opt.add( m_str[i] == '1' ? literal(v) : !literal(v));
    }
    bool res = solve();

//    if(res)
//    {
//        printf("Important Test:\n");
//        z3::model z3_model = opt.get_model();
//        z3::expr_vector z3_clause(c);
//        for (int v = 2; v <= num_variable; v++)
//        {
//            if(std::find(ind.begin(), ind.end(), v) != ind.end()) continue;
//            z3::func_decl decl(literal(v).decl());
//            z3::expr b = z3_model.get_const_interp(decl);
//            if (b.bool_value() == Z3_L_TRUE) z3_clause.push_back(!literal(v));
//            else z3_clause.push_back(literal(v));
//            opt.add(z3::mk_or(z3_clause));
//        }
//        bool newRes = solve();
//        if (newRes) printf("Failed\n");
//        else printf("good\n");
//
//    }

    opt.pop();
    return res;
}


