#include <stdlib.h>
#include "uthash/uthash.h"
#include "uthash/utarray.h"

#ifndef _SEQINDEX_H
#define _SEQINDEX_H

#define SUCCESS 0
#define SEQID_EXIST 11
#define SEQID_MISSING 12


#ifdef __cplusplus
extern "C" {
#endif

struct Seq
{
    char *seqid;
    char *seq;
    uint16_t *kmers; // kmers, 16 bit encoded
    uint8_t *ko; // kmer occurences
    size_t kn; // number of kmers
    UT_hash_handle hh;
};

struct SeqIndex
{
    struct Seq *seqs;
};

struct Search
{
    char **seqids;
    size_t n;
};

struct SeqIndex* init_seqindex();
void free_seqindex(struct SeqIndex *seqindex);
int add_seq(struct SeqIndex *seqindex, char *seqid, char *seq);
int remove_seq(struct SeqIndex *seqindex, char *seqid);
struct Search* search_seq(struct SeqIndex *seqindex, char *seq,
                          double similarity, size_t maxrejects);
struct Search* search_seq_prefix(struct SeqIndex *seqindex, char *seq);

double global_sim(char *seq1, char *seq2);

#ifdef __cplusplus
}
#endif

#endif /* _SEQINDEX_H */