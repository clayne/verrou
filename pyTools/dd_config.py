# This file is part of Verrou, a FPU instrumentation tool.

# Copyright (C) 2014-2021 EDF
#   F. Févotte <francois.fevotte@edf.fr>
#   B. Lathuilière <bruno.lathuiliere@edf.fr>


# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# 02111-1307, USA.

# The GNU Lesser General Public License is contained in the file COPYING.

import math
import gen_config

from pathlib import Path

def exponentialRange(nbRun):
    tab=[int(nbRun / (2**i)) for i in range(1+int(math.floor(math.log(nbRun,2)))) ]
    tab.reverse()
    return tab


class ddConfig(gen_config.gen_config):

    def __init__(self, argv, environ,config_keys=["INTERFLOP"], prefix="dd.generic"):
        self.prefix_=prefix
        super().__init__(argv, environ, config_keys)
        self.normalizeOptions()
        self.runScript=self.exec_arg[0]
        self.cmpScript=self.exec_arg[1]

    def registerOptions(self):
        self.addRegistry("cacheRep",              "string",     "REP",                     ["--rep="],                    self.prefix_,         None)
        self.addRegistry("nbRUN",                 "int",        "NRUNS",                   ["--nruns="],                  5,          None)
        self.addRegistry("maxNbPROC",             "int",        "NUM_THREADS",             ["--num-threads="],            None,       None)
        self.addRegistry("ddAlgo",                "string",     "ALGO",                    ["--algo="],                   "rddmin",   ["ddmax", "rddmin"])
        self.addRegistry("rddminVariant",         "string",     "RDDMIN",                  ["--rddmin="],                 "d",        ["s", "stoch", "d", "dicho", "", "strict"])
        self.addRegistry("param_rddmin_tab",      "string",     "RDDMIN_TAB",              ["--rddmin-tab="],             "exp",      ["exp", "all", "single"])
        self.addRegistry("param_dicho_tab",       "int/string", "DICHO_TAB" ,              ["--dicho-tab="],              "half",     ["exp", "all", "half", "single"])
        self.addRegistry("splitGranularity",      "int",        "DICHO_GRANULARITY",       ["--dicho-granularity="],       2,         None)
        self.addRegistry("ddQuiet",               "bool",       "QUIET",                   ["--quiet"],                    False,     None)
        self.addRegistry("cache",                 "string",     "CACHE" ,                  ["--cache="] ,                  "continue",["clean", "rename", "rename_keep_result","keep_run", "continue"])
        self.addRegistry("rddminHeuristicsCache", "string",     "RDDMIN_HEURISTICS_CACHE", ["--rddmin-heuristics-cache="], "none",    ["none", "cache", "all_cache"])
        self.addRegistry("rddminHeuristicsRep"  , "string",     "RDDMIN_HEURISTICS_REP",   ["--rddmin-heuristics-rep="],   [] ,       "rep_exists", True)
        self.addRegistry("rddminHeuristicsFile" , "string",     "RDDMIN_HEURISTICS_FILE",  ["--rddmin-heuristics-file="],   [] ,       "file_exists", True)
        self.addRegistry("rddminHeuristicsLineConv" , "bool",   "RDDMIN_HEURISTICS_LINE_CONV",    ["--rddmin-heuristics-line-conv"],     False,     None)
        self.addRegistry("resWithAllSamples"    , "bool",       "RES_WITH_ALL_SAMPLES",    ["--res-with-all-samples"],     False,     None)
        self.addRegistry("ddSeed"               ,  int,         "SEED",                 ["--seed="],                 None,      None)
        self.addRegistry("debug", "bool", "DEBUG",["--debug"], False, None)

    def normalizeOptions(self):
        if self.rddminVariant=="stoch":
            self.rddminVariant="s"
        if self.rddminVariant=="dicho":
            self.rddminVariant="d"
        if self.rddminVariant=="strict":
            self.rddminVariant=""

    def get_ddSeed(self):
        return self.ddSeed

    def get_cacheRep(self):
        return Path(self.cacheRep)

    ## Accessors
    def get_splitGranularity(self):
        return self.splitGranularity

    def get_ddAlgo(self):
        if self.ddAlgo.endswith("rddmin"):
            return self.rddminVariant+self.ddAlgo
        return self.ddAlgo

    def get_maxNbPROC(self):
        return self.maxNbPROC

    def get_nbRUN(self):
        return self.nbRUN

    def get_quiet(self):
        return self.ddQuiet

    def get_resWithAllsamples(self):
        return self.resWithAllSamples

    def get_rddMinTab(self):
        rddMinTab=None
        nbProc=1
        if self.maxNbPROC!=None:
            nbProc=self.maxNbPROC
        if self.param_rddmin_tab=="exp":
            if nbProc >self.nbRUN:
                return [self.nbRUN]
            else:
                return [x for x in exponentialRange(self.nbRUN) if x>=nbProc]
        if self.param_rddmin_tab=="all":
            if nbProc>self.nbRUN:
                return range(1,self.nbRUN+1)
            else:
                return range(nbProc, self.nbRUN+1)
        if self.param_rddmin_tab=="single":
            rddMinTab=[self.nbRUN]
        return rddMinTab

    def get_splitTab(self):
        splitTab=None
        if self.param_dicho_tab=="exp":
            splitTab=exponentialRange(self.nbRUN)
        if self.param_dicho_tab=="all":
            splitTab=range(self.nbRUN)
        if self.param_dicho_tab=="single":
            splitTab=[self.nbRUN]
        if self.param_dicho_tab=="half":
            splitTab=[ int(math.ceil(self.nbRUN / 2.))]
        if self.param_dicho_tab in [str(i) for i in range(1, self.nbRUN+1) ]:
            splitTab=[self.param_dicho_tab]
        return splitTab

    def get_runScript(self):
        return Path(self.runScript)

    def get_cmpScript(self):
        return Path(self.cmpScript)

    def get_cache(self):
        return self.cache

    def get_rddminHeuristicsCache(self):
        return self.rddminHeuristicsCache

    def get_rddminHeuristicsRep_Tab(self):
        return [Path(x) for x in self.rddminHeuristicsRep]

    def get_rddminHeuristicsFile_Tab(self):
        return [Path(x) for x in self.rddminHeuristicsFile]

    def get_rddminHeuristicsLineConv(self):
        return self.rddminHeuristicsLineConv

    def get_use_dd_min_par(self):
        return True #False #not yet efficient
