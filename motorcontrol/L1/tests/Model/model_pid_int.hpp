/*
 * Copyright 2022 Xilinx, Inc.
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
#ifndef _MODEL_PID_INT_HPP_
#define _MODEL_PID_INT_HPP_
#include "model_base.hpp"
template <class T_IN, class T_MID, class T_OUT, int MAX_OUT, int MIN_OUT, int KP_SCALE>
void PID_Control_T2(T_OUT& Res_out,
                    T_MID& GiE_prev,
                    T_MID& Err_prev,
                    T_IN in_data,
                    T_IN Sp,
                    T_IN Kp,
                    T_IN Ki,
                    T_IN Kd,
                    bool mode_change) {
    T_MID err = Sp - in_data;
    T_MID acc = GiE_prev + err;
    T_MID diff = err - Err_prev;
    T_MID P = Kp * err;
    T_MID I = Ki * acc;
    T_MID D = Kd * diff;
    T_MID sum = (P + I + D) >> KP_SCALE;
    T_MID out = in_data + sum;
    if (out > MAX_OUT)
        Res_out = MAX_OUT;
    else if (out < MIN_OUT)
        Res_out = MIN_OUT;
    else
        Res_out = out;
    Err_prev = err;
    GiE_prev = mode_change == true ? err : acc;
}

template <class t_float>
class Model_pid_int : public Model_base {
   public:
    enum TYPE_PARA {
        PID_DIN = 0,
        PID_SP,
        PID_KP,
        PID_KI,
        PID_KD,
        PID_ERR_PRE,
        PID_ACC,
        PID_ERR,
        PID_DIFF,
        PID_P,
        PID_I,
        PID_D,
        PID_SUM,
        PID_BIAS,
        PID_OUT
    };
    // input record
    t_float* input_m_din;
    t_float m_din;
    // pre-set parameters
    t_float m_sp;
    t_float m_kp;
    t_float m_ki;
    t_float m_kd;
    t_float m_bias;
    // t_float m_scl;
    // states
    t_float m_err_pre;
    t_float m_acc;
    // instantaneous variables
    t_float m_err;
    t_float m_diff;
    t_float m_P;
    t_float m_I;
    t_float m_D;
    t_float m_sum;
    t_float m_out;
    t_float* output_m_out;

    Model_pid_int() {
        id_type = MODEL_PID;
        num_models = 0;
        Model_base::num_para = TYPE_PARA::PID_OUT + 1;
        str_names[PID_DIN] = "PID_DIN    ";
        str_names[PID_SP] = "PID_SP     ";
        str_names[PID_KP] = "PID_KP     ";
        str_names[PID_KI] = "PID_KI     ";
        str_names[PID_KD] = "PID_KD     ";
        str_names[PID_ERR_PRE] = "PID_ERR_PRE";
        str_names[PID_ACC] = "PID_ACC    ";
        str_names[PID_ERR] = "PID_ERR    ";
        str_names[PID_DIFF] = "PID_DIFF   ";
        str_names[PID_P] = "PID_P      ";
        str_names[PID_I] = "PID_I      ";
        str_names[PID_D] = "PID_D      ";
        str_names[PID_SUM] = "PID_SUM    ";
        str_names[PID_BIAS] = "PID_BIAS   ";
        str_names[PID_OUT] = "PID_OUT    ";
        input_m_din = NULL;
        output_m_out = NULL;
        m_err_pre = 0;
        m_acc = 0;
        m_sp = 0;
        m_kp = 256;
        m_ki = 0;
        m_kd = 0;
        m_bias = 0;
        init_ParaType();
    }
    void init_ParaType() {
        for (int i = 0; i < num_para; i++) list_paraType[i] = T_INT;
    };
    void setPara(t_float sp_in, t_float kp_in, t_float ki_in, t_float kd_in) {
        m_sp = sp_in;
        m_kp = kp_in;
        m_kd = kd_in;
        m_ki = ki_in;
    }
    void stop() {
        m_err_pre = 0.0;
        m_acc = 0.0;
        m_err = 0.0;
        m_diff = 0.0;
        m_out = 0.0;
        m_P = 0.0;
        m_I = 0.0;
        m_D = 0.0;
        m_sum = 0.0;
    }
    void pullInput() {
        assert(input_m_din != NULL);
        m_din = *input_m_din;
    }
    void pushOutput() {
        if (output_m_out != NULL)
            ;
        *output_m_out = m_out;
    }
    void setInput(t_float din) { m_din = din; }
    void getOutput(t_float& out) { out = m_out; }

    void updating_org(double dt) {
        t_cur += dt;
        m_err = m_sp - m_din;
        m_acc += m_err;
        m_diff = m_err - m_err_pre;
        m_P = m_kp * m_err;
        m_I = m_ki * m_acc;
        m_D = m_kd * m_diff;
        m_sum = (m_P + m_I + m_D) >> 8;
        m_out = m_din + m_sum + m_bias;
        m_err_pre = m_err;
    }

    void updating_noin(double dt) {
        t_cur += dt;
        m_err = m_sp - m_din;
        m_acc += m_err;
        m_diff = m_err - m_err_pre;
        m_P = m_kp * m_err;
        m_I = m_ki * m_acc;
        m_D = m_kd * m_diff;
        m_sum = (m_P + m_I + m_D) >> 8;
        m_out = m_sum + m_bias;
        m_err_pre = m_err;
    }

    void updating(double dt) {
        t_cur += dt;
        PID_Control_T2<int, int, int, 32767, -32767, 8>(m_out, m_acc, m_err_pre, m_din, m_sp, m_kp, m_ki, m_kd, false);
    }

    void updating_noin2(double dt) {
        t_cur += dt;
        m_err = m_sp - m_din;
        m_acc += m_err;
        m_diff = m_err - m_err_pre;
        m_P = m_kp * m_err;
        m_I = (m_ki * m_acc) >> 8;
        m_D = (m_kd * m_diff) >> 8;
        m_sum = (m_P + m_I + m_D) >> 8;
        m_out = m_sum + m_bias;
        m_err_pre = m_err;
    }

    void init_pPara() {
        Model_base::init_pPara();
        list_pPara[PID_DIN] = &m_din;
        list_pPara[PID_SP] = &m_sp;
        list_pPara[PID_KP] = &m_kp;
        list_pPara[PID_KI] = &m_ki;
        list_pPara[PID_KD] = &m_kd;
        list_pPara[PID_ERR_PRE] = &m_err_pre;
        list_pPara[PID_ERR] = &m_err;
        list_pPara[PID_ACC] = &m_acc;
        list_pPara[PID_DIFF] = &m_diff;
        list_pPara[PID_P] = &m_P;
        list_pPara[PID_I] = &m_I;
        list_pPara[PID_D] = &m_D;
        list_pPara[PID_SUM] = &m_sum;
        list_pPara[PID_BIAS] = &m_bias;
        list_pPara[PID_OUT] = &m_out;
    }

    void prepareScreen() {
        sprintf(str_screen[PID_DIN], "%s : %d", str_names[PID_DIN], m_din);
        sprintf(str_screen[PID_SP], "%s : %d", str_names[PID_SP], m_sp);
        sprintf(str_screen[PID_KP], "%s : %d", str_names[PID_KP], m_kp);
        sprintf(str_screen[PID_KI], "%s : %d", str_names[PID_KI], m_ki);
        sprintf(str_screen[PID_KD], "%s : %d", str_names[PID_KD], m_kd);
        sprintf(str_screen[PID_ERR_PRE], "%s : %d", str_names[PID_ERR_PRE], m_err_pre);
        sprintf(str_screen[PID_ERR], "%s : %d", str_names[PID_ERR], m_err);
        sprintf(str_screen[PID_ACC], "%s : %d", str_names[PID_ACC], m_acc);
        sprintf(str_screen[PID_DIFF], "%s : %d", str_names[PID_DIFF], m_diff);
        sprintf(str_screen[PID_P], "%s : %d", str_names[PID_P], m_P);
        sprintf(str_screen[PID_I], "%s : %d", str_names[PID_I], m_I);
        sprintf(str_screen[PID_D], "%s : %d", str_names[PID_D], m_D);
        sprintf(str_screen[PID_SUM], "%s : %d", str_names[PID_SUM], m_sum);
        sprintf(str_screen[PID_BIAS], "%s : %d", str_names[PID_BIAS], m_bias);
        sprintf(str_screen[PID_OUT], "%s : %d", str_names[PID_OUT], m_out);
    }
    void printParameters(FILE* fp, int line) {
        bool isTitle = line == -1 ? true : false;
        isTitle ? fprintf(fp, "m_din\t") : fprintf(fp, "%d\t", m_din);
        isTitle ? fprintf(fp, "m_sp\t") : fprintf(fp, "%d\t", m_sp);
        isTitle ? fprintf(fp, "m_kp\t") : fprintf(fp, "%d\t", m_kp);
        isTitle ? fprintf(fp, "m_ki\t") : fprintf(fp, "%d\t", m_ki);
        isTitle ? fprintf(fp, "m_kd\t") : fprintf(fp, "%d\t", m_kd);
        isTitle ? fprintf(fp, "m_err\t") : fprintf(fp, "%d\t", m_err);
        isTitle ? fprintf(fp, "m_acc\t") : fprintf(fp, "%d\t", m_acc);
        isTitle ? fprintf(fp, "m_diff\t") : fprintf(fp, "%d\t", m_diff);
        isTitle ? fprintf(fp, "m_P\t") : fprintf(fp, "%d\t", m_P);
        isTitle ? fprintf(fp, "m_I\t") : fprintf(fp, "%d\t", m_I);
        isTitle ? fprintf(fp, "m_D\t") : fprintf(fp, "%d\t", m_D);
        isTitle ? fprintf(fp, "m_sum\t") : fprintf(fp, "%d\t", m_sum);
        isTitle ? fprintf(fp, "m_out\t") : fprintf(fp, "%d\t", m_out);
    }
};
#endif