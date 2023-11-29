#pragma once

#ifndef INTERFLOP_STATIC_INTERFACE_ENABLED
#error "INTERFLOP_STATIC_INTERFACE_ENABLED should be defined"
#endif
#include "interflop_verrou/interflop_verrou.h"
#ifdef USE_VERROU_QUAD
#include "backend_mcaquad/interflop_mcaquad.h"
#else
#define MCAMODE_IEEE 0
#define MCAMODE_MCA  1
#define MCAMODE_PB   2
#define MCAMODE_RR   3
#endif
#include "backend_checkcancellation/interflop_checkcancellation.h"
#include "backend_checkdenorm/interflop_checkdenorm.h"
#include "backend_check_float_max/interflop_check_float_max.h"
