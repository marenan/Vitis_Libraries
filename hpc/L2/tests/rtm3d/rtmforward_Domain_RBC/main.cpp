/*
 * Copyright 2019 Xilinx, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/

#include <chrono>
#include <cmath>
#include <cstdlib>
#include <cassert>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <vector>
#include "rtm3d.hpp"
#include "types.hpp"
#include "utils.hpp"
using namespace std;

typedef WideData<RTM_dataType, RTM_nPEX> RTM_wideTypeX;
typedef WideData<RTM_wideTypeX, RTM_nPEZ> RTM_wideType;

int main(int argc, char** argv) {
    int err5 = 0, err6 = 0, err7 = 0;
    bool pass5, pass6, pass7 = true;

    const int requiredArg = 7;
    if (argc < requiredArg) return EXIT_FAILURE;

    unsigned int argId = 0;

    string l_xclbinFile(argv[++argId]);
    string filePath = argv[++argId];
    int l_z = atoi(argv[++argId]);
    int l_y = atoi(argv[++argId]);
    int l_x = atoi(argv[++argId]);
    int l_time = atoi(argv[++argId]);
    int l_shot = 1;

    int l_imgX = l_x - 2 * RTM_NXB;
    int l_imgY = l_y - 2 * RTM_NYB;
    int l_imgZ = l_z - 2 * RTM_NZB;
    int l_cube = l_x * l_y * l_z;

    bool l_verify = false;
    if (argc > 1 + argId) l_verify = atoi(argv[++argId]) == 0 ? false : true;

    unsigned int l_deviceId = 0;
    if (argc > 1 + argId) l_deviceId = atoi(argv[++argId]);

    assert(l_time % RTM_numFSMs == 0);
    assert(l_z % RTM_nPEZ == 0);
    assert(l_x % RTM_nPEX == 0);
    assert(l_z <= RTM_maxZ);

    host_buffer_t<RTM_wideType> l_snap0, l_snap1;
    vector<RTM_dataType> p, pp, snap0, snap1, ref;

    p.resize(l_cube);
    pp.resize(l_cube);

    FPGA fpga(l_deviceId);
    fpga.xclbin(l_xclbinFile);
    ForwardKernel<RTM_dataType, RTM_order, RTM_nPEZ, RTM_nPEX> fwd(&fpga, l_z, l_y, l_x, RTM_NZB, RTM_NYB, RTM_NXB,
                                                                   l_time, l_shot);

    fwd.loadData(filePath);
    double elapsedF = 0;

    bool selF = (l_time / RTM_numFSMs) % 2 == 0;
    auto start = chrono::high_resolution_clock::now();
    for (int s = 0; s < l_shot; s++) {
        elapsedF += fwd.run(selF, s, l_y / 2, l_x / 2, l_snap0, l_snap1);

        if (l_verify) {
            converter<RTM_nPEX, RTM_nPEZ>(l_x, l_y, l_z, l_snap0.data(), pp);
            converter<RTM_nPEX, RTM_nPEZ>(l_x, l_y, l_z, l_snap1.data(), p);

            readBin(filePath + "snap0.bin", sizeof(float) * l_cube, snap0);
            readBin(filePath + "snap1.bin", sizeof(float) * l_cube, snap1);

            pass5 = compare<RTM_dataType>(l_cube, pp.data(), snap0.data(), err5);
            cout << "There are in total " << err5 << " errors in pp v.s. snap0" << endl;

            pass6 = compare<RTM_dataType>(l_cube, p.data(), snap1.data(), err6);
            cout << "There are in total " << err6 << " errors in p v.s. snap1" << endl;

            if (pass5 && pass6) {
                cout << "Test passed!" << endl;
            } else {
                cout << "Test failed, there are in total " << err5 + err6 << " errors!" << endl;
                return EXIT_FAILURE;
            }
        }
    }
    auto finish = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = finish - start;

    cout << "Execution completed" << endl;
    cout << "Average forward execution time " << elapsedF / l_shot << "s." << endl;
    cout << "Average total execution time " << elapsed.count() / l_shot << "s." << endl;

    if (pass7)
        return EXIT_SUCCESS;
    else
        return EXIT_FAILURE;
}
