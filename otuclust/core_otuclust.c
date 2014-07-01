/*     
    This code is written by Davide Albanese <davide.albanese@gmail.com>.
    Copyright (C) 2013 Davide Albanese
    Copyright (C) 2013 Fondazione Edmund Mach.
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include "uthash/uthash.h"
#include "uthash/utarray.h"
#include "core_otuclust.h"


#define MATCH 0
#define MISMATCH 1
#define GAP 1

#define S(a, b) ((a)==(b)?(MATCH):(MISMATCH))
#define MIN(a, b) ((a)<(b)?(a):(b))
#define MAX(a, b) ((a)>(b)?(a):(b))

#define KMER_LEN 7 // must be <= 8


char* scopy(char *s)
{
    char *sc = (char *) malloc ((strlen(s)+1) * sizeof(char));
    strcpy(sc, s);

    return sc;
}


double global_sim(char *seq1, char *seq2)
{
    int **cost; // cost matrix
    char **back; // backtracking matrix
    int i, j, n, m;
    int d, u, l;
    int matches=0, mismatches=0;


    n = strlen(seq1);
    m = strlen(seq2);

    cost = (int **) malloc ((n+1) * sizeof(int *));
    back = (char **) malloc ((n+1) * sizeof(char *));
    for (i=0; i<=n; i++)
    {
        cost[i] = (int *) malloc ((m+1) * sizeof(int));
        back[i] = (char *) malloc ((m+1) * sizeof(char));
    }

    /* fill cost and back */
    cost[0][0] = 0;
    back[0][0] = 'D';
    for (i=1; i<=n; i++)
    {
        cost[i][0] = i * GAP;
        back[i][0] = 'U'; /* Up */
    }
    for (j=1; j<=m; j++)
    {
        cost[0][j] = j * GAP;
        back[0][j] = 'L'; /* Left */
    }
    for (i=1; i<=n; i++)
    {
        for (j=1; j<=m; j++)
        {
            d = cost[i-1][j-1] + S(seq1[i-1], seq2[j-1]);
            u = cost[i-1][j] + GAP;
            l = cost[i][j-1] + GAP;
            cost[i][j] = MIN(MIN(u, l), d);

            if (cost[i][j] == l)
                back[i][j] = 'L';
            else if (cost[i][j] == u)
                back[i][j] = 'U';
            else if (cost[i][j] == d)
                back[i][j] = 'D';
           }
    }

    /* traceback */
    i = n; j = m;
    while (i > 0 || j > 0)
    {
        if (back[i][j] == 'D')
        {
            if (seq1[i-1] == seq2[j-1])
                matches++;
            else
                mismatches++;

            i--; j--;
        }
        else if (back[i][j] == 'U')
            i--;
        else if (back[i][j] == 'L')
            j--;
    }

    for (i=0; i<=n; i++)
    {
        free(cost[i]);
        free(back[i]);
    }
    free(cost);
    free(back);

    return (double)matches / (double)(matches+mismatches);
}


struct KSearch
{
    char *seqid;
    char *seq;
    double ksim; // kmer similarity
    UT_hash_handle hh;
};


uint16_t nucl2four(char n)
{
    switch(n)
    {
        case 'A':
            return 0;
        case 'C':
            return 1;
        case 'G':
            return 2;
        case 'T':
            return 3;
        default:
            return 0;
    }
}


uint16_t kmer2uint16(char *kmer)
{
    uint16_t i, num=0;
    for (i=0; i<KMER_LEN; i++)
    {
        num *= 4;
        num += nucl2four(kmer[i]);
    }

    return num;
}


int compare_uint16(const void *a, const void *b)
{
    const uint16_t *ia = (const uint16_t *) a;
    const uint16_t *ib = (const uint16_t *) b;

    if (*ia > *ib)
        return 1;
    else if (*ia < *ib)
        return -1;
    else
        return 0;
}


size_t unique_uint16(uint16_t *a, size_t len, uint16_t **ua, uint8_t **un)
{
    size_t i, ulen;

    *ua = NULL;
    if (len <= 0)
        return 0;

    qsort (a, len, sizeof(uint16_t), compare_uint16);

    *ua = (uint16_t *) malloc (sizeof(uint16_t));
    *un = (uint8_t *) malloc (sizeof(uint8_t));
    (*ua)[0] = a[0];
    (*un)[0] = 1;
    ulen = 1;
    for (i=1; i<len; i++)
        if (a[i] != (*ua)[ulen-1])
        {
            *ua = (uint16_t *) realloc (*ua, (ulen+1)*sizeof(uint16_t));
            *un = (uint8_t *) realloc (*un, (ulen+1)*sizeof(uint8_t));
            (*ua)[ulen] = a[i];
            (*un)[ulen] = 1;
            ulen++;
        }
        else
        {
            if((*un)[ulen-1] < UINT8_MAX)
                (*un)[ulen-1]++;
        }

    return ulen;
}


size_t common_kmers(struct Seq *seq1, struct Seq *seq2)
{
    size_t i, j, c;

    i = 0; j = 0; c = 0;
    while (i<seq1->kn && j<seq2->kn)
    {
        if (seq1->kmers[i] < seq2->kmers[j])
            i++;
        else if (seq1->kmers[i] > seq2->kmers[j])
            j++;
        else
        {
            c += 1;
            i++; j++;
        }
    }

    return c;
}


double kmer_sim(struct Seq *seq1, struct Seq *seq2)
{
    size_t i, j, s, d;


    i = 0; j = 0; s = 0;
    while (i<seq1->kn && j<seq2->kn)
    {
        if (seq1->kmers[i] < seq2->kmers[j])
            i++;
        else if (seq1->kmers[i] > seq2->kmers[j])
            j++;
        else
        {
            s += MIN(seq1->ko[i], seq2->ko[j]);
            i++; j++;
        }
    }

    d = MIN(strlen(seq1->seq), strlen(seq2->seq)) - KMER_LEN + 1;
    return (double)s / (double)d;
}


// decreasing order
int compare_ksearch(const void *a, const void *b)
{
    const struct KSearch *ia = (const struct KSearch *) a;
    const struct KSearch *ib = (const struct KSearch *) b;

    if (ia->ksim < ib->ksim)
        return 1;
    else if (ia->ksim > ib->ksim)
        return -1;
    else
        return 0;
}


struct Seq* init_seq(char *seqid, char *seq)
{
    size_t i, kn, seqlen;
    uint16_t *tmp;

    struct Seq *s = (struct Seq*) malloc (sizeof(struct Seq));
    s->seqid = scopy(seqid);
    s->seq = scopy(seq);
    s->kmers = NULL;
    s->ko = NULL;
    s->kn = 0;

    seqlen = strlen(s->seq);
    if (KMER_LEN > seqlen)
        return s;

    // find kmers (with duplicates)
    kn = seqlen-KMER_LEN+1;
    tmp = (uint16_t *) malloc (kn * sizeof(uint16_t));
    for (i=0; i<kn; i++)
        tmp[i] = kmer2uint16(s->seq+i);

    // remove duplicates and count kmersoccurrences
    s->kn = unique_uint16(tmp, kn, &s->kmers, &s->ko);

    free(tmp);
    return s;
}


void free_seq(struct Seq *seq)
{
    free(seq->seqid);
    free(seq->seq);
    free(seq->kmers);
    free(seq->ko);
    free(seq);
}


struct SeqIndex* init_seqindex()
{
    struct SeqIndex *seqindex = (struct SeqIndex*) malloc (sizeof(struct
                                                           SeqIndex));
    seqindex->seqs = NULL;
    return seqindex;
}


void free_seqindex(struct SeqIndex *seqindex)
{
    struct Seq *si, *sitmp;

    HASH_ITER(hh, seqindex->seqs, si, sitmp)
    {
        HASH_DEL(seqindex->seqs, si);
        free_seq(si);
    }

    free(seqindex);
}


int add_seq(struct SeqIndex *seqindex, char *seqid, char *seq)
{
    struct Seq *s;

    HASH_FIND_STR(seqindex->seqs, seqid, s);
    if (s == NULL)
    {
        s = init_seq(seqid, seq);
        HASH_ADD_KEYPTR(hh, seqindex->seqs, s->seqid, strlen(s->seqid), s);
    }
    else
        return SEQID_EXIST;

    return SUCCESS;
}


int remove_seq(struct SeqIndex *seqindex, char *seqid)
{
    struct Seq *s;

    HASH_FIND_STR(seqindex->seqs, seqid, s);
    if (s == NULL)
        return SEQID_MISSING;
    else
    {
        HASH_DEL(seqindex->seqs, s);
        free_seq(s);
    }

    return SUCCESS;
}


struct Search* search_seq(struct SeqIndex *seqindex, char *seq,
                          double similarity, size_t maxrejects)
{
    struct Seq *q, *t;
    struct KSearch *ksearch=NULL, *ks, *kstmp;
    struct Search *search;
    size_t rejects;
    double gsim, ksim;

    q = init_seq("", seq);

    for(t=seqindex->seqs; t!=NULL; t=t->hh.next)
    {
        ksim = kmer_sim(q, t);
        ks = (struct KSearch*) malloc (sizeof (struct KSearch));
        ks->seqid = t->seqid;
        ks->seq = t->seq;
        ks->ksim = ksim;
        HASH_ADD_KEYPTR(hh, ksearch, ks->seqid, strlen(ks->seqid), ks);
    }

    free_seq(q);

    // decreasing order
    HASH_SORT(ksearch, compare_ksearch);

    search = (struct Search*) malloc (sizeof(struct Search));
    search->seqids = NULL;
    search->n = 0;
    rejects = 0;
    for(ks=ksearch; ks!=NULL; ks=ks->hh.next)
    {
        gsim = global_sim(seq, ks->seq);
        if (gsim < similarity)
            rejects++;
        else
        {
            search->n += 1;
            search->seqids = (char **) realloc (search->seqids,
                                                search->n * sizeof (char *));
            search->seqids[search->n-1] =
                (char *) malloc ((strlen(ks->seqid)+1) * sizeof (char));
            strcpy(search->seqids[search->n-1], ks->seqid);
            rejects = 0;
        }

        if (rejects == maxrejects)
            break;
    }

    HASH_ITER(hh, ksearch, ks, kstmp)
    {
        HASH_DEL(ksearch, ks);
        free(ks);
    }

    return search;
}


struct Search* search_seq_prefix(struct SeqIndex *seqindex, char *seq)
{
    struct Seq *t;
    struct Search *search;
    size_t seqlen;

    seqlen = strlen(seq);

    search = (struct Search*) malloc (sizeof(struct Search));
    search->seqids = NULL;
    search->n = 0;
    for(t=seqindex->seqs; t!=NULL; t=t->hh.next)
    {
        if (strlen(t->seq) >= seqlen)
        {
            if (!strncmp(seq, t->seq, seqlen))
            {
                search->n += 1;
                search->seqids = (char **) realloc (search->seqids,
                                                search->n * sizeof (char *));
                search->seqids[search->n-1] =
                    (char *) malloc ((strlen(t->seqid)+1) * sizeof (char));
                strcpy(search->seqids[search->n-1], t->seqid);
            }
        }
    }

    return search;
}
