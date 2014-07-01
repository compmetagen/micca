import numpy as np
cimport numpy as np
from libc.stdlib cimport *
cimport cython


cdef extern from "core_otuclust.h":
    cdef int SUCCESS
    cdef int SEQID_EXIST
    cdef int SEQID_MISSING

    cdef struct Seq

    struct SeqIndex:
        Seq *seqs

    struct Search:
        char **seqids
        size_t n

    SeqIndex* init_seqindex()
    void free_seqindex(SeqIndex *seqindex)
    int add_seq(SeqIndex *seqindex, char *seqid, char *seq)
    int remove_seq(SeqIndex *seqindex, char *seqid)
    Search* search_seq(SeqIndex *seqindex, char *seq, double similarity, \
                       size_t maxrejects)
    Search* search_seq_prefix(SeqIndex *seqindex, char *seq)

    double global_sim(char *seq1, char *seq2)


cdef class SI:
    """
    """

    cdef SeqIndex *seqindex

    def __cinit__(self):
        """
        """

        self.seqindex = init_seqindex()

    def add(self, seqid, seq):
        """
        """
        cdef int ret

        ret = add_seq(self.seqindex, seqid, seq)
        if ret == SEQID_EXIST:
            raise ValueError("seqid %s already exist" % seqid)

    def remove(self, seqid):
        """
        """
        cdef int ret

        ret = remove_seq(self.seqindex, seqid)
        if ret == SEQID_MISSING:
            raise ValueError("missing seqid %s" % seqid)


    def search(self, seq, similarity=0.97, maxrejects=32):
        cdef size_t i
        cdef Search *sh

        sh = search_seq(self.seqindex, seq, similarity, maxrejects)
        ret = []
        for i in range(sh.n):
            ret.append(sh.seqids[i])
            free(sh.seqids[i])
        free(sh.seqids)
        free(sh)

        return ret

    def search_prefix(self, seq):
        cdef size_t i
        cdef Search *sh

        sh = search_seq_prefix(self.seqindex, seq)
        ret = []
        for i in range(sh.n):
            ret.append(sh.seqids[i])
            free(sh.seqids[i])
        free(sh.seqids)
        free(sh)

        return ret

    cdef void _free_seqindex(self):
        free_seqindex(self.seqindex)

    def __dealloc__(self):
        self._free_seqindex()


def gsim(seq1, seq2):
    return global_sim(seq1, seq2)