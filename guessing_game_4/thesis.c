#include <stdio.h>
#include <malloc.h>
#include <assert.h>
#include <values.h>
#include <math.h>

#define NMAX 126
#define EMAX 32
#define FEXP(n) (pow(2.0, (double)(n)))

typedef struct winstate
{
    struct winstate *next;
    int ns;
    struct winstate *left, *right;
    int state[EMAX + 1];
} winstate;

#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define MIN(a, b) ((a) < (b) ? (a) : (b))
static double bico[128][128], wts[128][128];
static winstate *tree[NMAX + 1];
static int mcurrent;
static int leafnodes, safeleaves;
static int treenodes, searchnodes;

int treesearch(int e, int n, int m);
int lifttree(int e, int n, int m);
winstate *depthsearch(int state[], int ns, int n);
void inittree(void);
winstate *addtree(int state[], int ns, int n,
                  winstate *left, winstate *right);
winstate *cachetest(int state[], int ns, int n);
void cleartree(void);
int igcd(int m, int n);
void initwts(void);
double weight(int state[], int ns, int n);
int stateleq(int state1[], int ns1, int state2[], int ns2);
int mbound(int m, int e);
void copystate(int copy[], int *nc, int state[], int ns);
int leaftest(int state[], int *nsp, int n, int *safe);
int sumtest(int sum[], int ns,
            int state1[], int ns1, int state2[], int ns2);
void addstate(int sum[], int *nsp,
              int state1[], int ns1, int state2[], int ns2);

int main(int argc, char **argv)
{
    int win;
    int e, k, m, n;
    setvbuf(stdout, NULL, _IOLBF, BUFSIZ);
    setvbuf(stderr, NULL, _IOLBF, BUFSIZ);
    initwts();
    inittree();
    
    printf("\n2048 - 15 - 1 output:\n");
    (void)treesearch(1, 15, 2048);
    printf("\n4096 - 23 - 3 output:\n");
    (void)treesearch(3, 23, 4096);

    return 0;
}


// e = NUMBER_OF_LIES, n = NUMBER_OF_GUESSES, m = MAX_NUMBER
int treesearch(int e, int n, int m)
{
    int state[EMAX + 1], ns;
    winstate *wp;
    int j;
    cleartree();
    ns = e + 1;
    for (j = 0; j < e; j++)
        state[j] = 0;
    state[e] = m;
    mcurrent = m;
    leafnodes = safeleaves = 0;
    wp = depthsearch(state, ns, n);
    printf("E=%d N=%d M=%d: ", e, n, m);
    if (wp != 0)
    {
        printf("OK, %d tree nodes, %d leaf nodes (%d safe).\n",
               treenodes, leafnodes, safeleaves);
        return 1;
    }
    else
    {
        printf("Failed, %d search nodes.\n", searchnodes);
        return 0;
    }
}
int lifttree(int e, int n, int m)
{
    int state[EMAX + 1];
    winstate *wp;
    int safe;
    int ns, nn;
    while (leafnodes > safeleaves)
    {
        e += 1;
        n += 3;
        printf("E=%d N=%d M=%d: ", e, n, m);
        leafnodes = safeleaves = 0;
        for (nn = n; nn >= 3; nn--)
        {
            tree[nn] = tree[nn - 3];
            tree[nn - 3] = 0;
        }
        for (nn = 3; nn <= n; nn++)
        {
            for (wp = tree[nn]; wp != 0; wp = wp->next)
            {
                


                state[0] = 0;
                copystate(state + 1, &ns, wp->state, wp->ns);
                ns++;
                if (wp->left == 0)
                {
                    if (!leaftest(state, &ns, nn, &safe))
                        goto FAIL;
                    leafnodes++;
                    if (safe)
                        safeleaves++;
                }
                else
                {
                    if (!sumtest(state, ns, wp->left->state, wp->left->ns,
                                 wp->right->state, wp->right->ns))
                    {
                        state[0] = 1;
                        ns = 1;
                    }
                    addstate(state, &ns, wp->left->state, wp->left->ns,
                             wp->right->state, wp->right->ns);
                }
                copystate(wp->state, &wp->ns, state, ns);
            }
        }
        if (tree[n]->state[e] != m)
        {
        FAIL:
            printf("lift failed.\n");
            return 0;
        }
        printf("lift succeeded: %d leaf nodes (%d safe).\n",
               leafnodes, safeleaves);
    }
    return (leafnodes == safeleaves);
}
winstate *depthsearch(int state[], int ns, int n)
{
    int cut[EMAX + 1], left[EMAX + 1], right[EMAX + 1], bias[EMAX + 1];
    int temp[EMAX + 1], nr, nt;
    double z, v, w, cmin, cmax;
    winstate *wp, *wpr, *wpl;
    int j, jj, k, nn, biaslvl, safe;
    searchnodes++;
    /* Cache check */
    wp = cachetest(state, ns, n);
    if (wp != 0)
        return wp;
    /* Check for leaf nodes */
    copystate(temp, &nt, state, ns);
    if (leaftest(temp, &nt, n, &safe))
    {
        leafnodes++;
        if (safe)
            safeleaves++;
        return addtree(temp, nt, n, 0, 0);
    }
    for (j = 0; j < ns; j++)
        bias[j] = 0;
    biaslvl = ns - 1;

    goto TRY;
RETRY:
    if (bias[biaslvl] < 0)
        bias[biaslvl] = -bias[biaslvl];
    else
        bias[biaslvl] = -bias[biaslvl] - 1;
    if (bias[biaslvl] <= -3)
    {
        bias[biaslvl] = 0;
        do
        {
            biaslvl--;
            if (biaslvl == 0)
                return 0;
        } while (state[biaslvl] == 0);
        bias[biaslvl] = -1;
    }
TRY:
    for (j = 0; j < ns; j++)
        left[j] = right[j] = 0;
    k = 0;
    for (j = ns - 1; j >= 0; j--)
    {
        if (state[j] == 0)
        {
            cut[j] = 0;
            continue;
        }
        k += state[j];
        if (k == 1)
        {
            if (bias[j] != 0)
                goto RETRY;
            cut[j] = 0;
            goto CUT;
        }
        if (k == 2)
        {
            cut[j] = 1 + bias[j];
            if (cut[j] < 0 || cut[j] > state[j])
                goto RETRY;
            goto CUT;
        }
        cmin = -MAXINT;
        cmax = MAXINT;
        for (jj = j; jj >= 0; jj--)
        {
            nn = n - 3 * jj - 1;
            v = FEXP(nn) - weight(left + jj, ns - jj, nn) -
                weight(state + jj + 1, j - jj, nn);
            /* Projected right gap if cut[0..j] == 0 */
            w = FEXP(nn) - weight(right + jj, ns - jj, nn) -
                weight(state + jj + 1, j - jj, nn);
            if (v < 0.0 || w < 0.0)
                goto RETRY;
            cmin = MAX(cmin, (state[j] - v / bico[nn][j - jj]));
            cmax = MIN(cmax, w / bico[nn][j - jj]);
        }
        if (cmin > cmax)
            goto RETRY;
        z = floor(0.5 * (cmin + cmax + 1));
        z = MAX(z, 0.0);
        z = MIN(z, state[j]);

        cut[j] = z + bias[j];

        if (cut[j] < cmin || cut[j] > cmax)
            goto RETRY;
    CUT:
        if (cut[j] < 0 || cut[j] > state[j])
            goto RETRY;
        left[j] += state[j] - cut[j];
        right[j] += cut[j];

        if (j > 0)
        {
            left[j - 1] += cut[j];
            right[j - 1] += state[j] - cut[j];
        }
    }
    nr = ns;

    while (nr > 0 && right[nr - 1] == 0)
        nr--;
    wpl = depthsearch(left, ns, n - 1);
    if (wpl == 0)
        goto RETRY;
    wpr = depthsearch(right, nr, n - 1);
    if (wpr == 0)
        goto RETRY;
    copystate(temp, &nt, state, ns);
    addstate(temp, &nt, wpl->state, wpl->ns, wpr->state, wpr->ns);
    return addtree(temp, nt, n, wpl, wpr);
}
void inittree()
{
    int n;
    for (n = 0; n <= NMAX; n++)
        tree[n] = 0;
    treenodes = 0;
}
winstate *addtree(int state[], int ns, int n, winstate *left, winstate *right)
{
    winstate *wp;
    int j;
    for (wp = tree[n]; wp != 0; wp = wp->next)
        if (stateleq(state, ns, wp->state, wp->ns))
        {
            return wp;
        }
    treenodes++;
    wp = tree[n];
    tree[n] = (winstate *)malloc(sizeof(winstate));
    tree[n]->next = wp;
    tree[n]->ns = ns;
    for (j = 0; j < ns; j++)
        tree[n]->state[j] = state[j];
    tree[n]->left = left;
    tree[n]->right = right;

    // Hook on to function to print tree solutions for how many of each guess-states to remove in each step
    const int MAX_PRINT_DEPTH = 23;

    winstate *wpi = tree[n];

    for(int i = 0; i < MAX_PRINT_DEPTH; i++)
    {
        printf("[step:%02i] [tree:%02i] state[0]: %i state[1]: %i state[2]: %i state[3]: %i\n", n, i, wpi->state[0], wpi->state[1], wpi->state[2], wpi->state[3]);

        if(wpi->next)
        {
            wpi = wpi->next;
        }
    }

    return tree[n];
}

winstate *cachetest(int state[], int ns, int n)
{
    winstate *wp;
    wp = tree[n];
    while (wp != 0)
    {
        if (stateleq(state, ns, wp->state, wp->ns))
            return wp;
        wp = wp->next;
    }
    return 0;
}

void cleartree()
{
    int n;
    winstate *wp, *wpnext;
    for (n = 0; n <= NMAX; n++)
    {
        wp = tree[n];
        while (wp != 0)
        {
            wpnext = wp->next;
            free(wp);
            wp = wpnext;
        }
        tree[n] = 0;
    }
    treenodes = 0;
    searchnodes = 0;
}

int igcd(int m, int n)
{
    if (m < 0)
        m = -m;
    if (n < 0)
        n = -n;
    if (m > n)
        return igcd(n, m);
    if (m == 0)
        return n;
    return igcd(n % m, m);
}

void initwts(void)
{
    int g, j, n;
    for (n = 0; n <= NMAX; n++)
    {
        bico[n][0] = 1.0;
        wts[n][0] = 1.0;
        for (j = 1; j <= n; j++)
        {
            g = igcd(n - j + 1, j);
            bico[n][j] = (bico[n][j - 1] / (j / g)) * ((n - j + 1) / g);
            wts[n][j] = wts[n][j - 1] + bico[n][j];
        }
    }
}

double weight(int state[], int ns, int n)
{
    double w;
    int j;
    w = 0.0;
    for (j = 0; j < ns; j++)
    {
        w += state[j] * wts[n][j];
    }
    return w;
}

int stateleq(int state1[], int ns1, int state2[], int ns2)
{
    int j, k1, k2;
    if (ns1 > ns2)
        return 0;
    k1 = k2 = 0;
    for (j = ns2 - 1; j > ns1 - 1; j--)
        k2 += state2[j];
    for (j = ns1 - 1; j >= 0; j--)
    {
        k1 += state1[j];
        k2 += state2[j];

        if (k2 >= mcurrent)
            return 1;
        if (k1 > k2)
            return 0;
    }
    return 1;
}

int mbound(int n, int e)
{
    int j, m;
    double z, zz;
    if (n < 2 * e + 1)
    {
        m = 1;
    }
    else if (n <= 3 * e)
    {
        m = 2;
    }
    else
    {
        z = FEXP(n) / wts[n][e];
        for (j = 1; j <= e; j++)
        {
            zz = FEXP(n - 3 * j) / wts[n - 3 * j][e - j];
            z = MIN(z, zz);
        }
        m = floor(z);
    }

    return m;
}

void copystate(int copy[], int *nc, int state[], int ns)
{
    int i;
    *nc = ns;
    for (i = 0; i < ns; i++)
        copy[i] = state[i];
}

int leaftest(int state[], int *nsp, int n, int *safe)
{
    int leafstate[EMAX + 2];
    double w;
    int i, k, nn, ns;
    ns = *nsp;
    nn = n - 3 * (ns - 1);

    if (nn > 4)
        return 0;
    leafstate[ns] = (nn >= 0) ? (1 << nn) : 1;
    for (i = 0; i < ns; i++)
        leafstate[i] = 0;
    k = leafstate[ns];
    for (i = 1; i < ns; i++)
    {
        nn += 3;
        if (nn < i + 1)
            continue;
        w = FEXP(nn) - weight(leafstate + (ns - i), i + 1, nn);

        if (w >= mcurrent - k)
        {
            leafstate[ns - i] = mcurrent - k;
            k = mcurrent;

            break;
        }
        leafstate[ns - i] = w;
        k += leafstate[ns - i];
    }
    if (!stateleq(state, ns, leafstate + 1, ns))
        return 0;
    copystate(state, nsp, leafstate + 1, ns);
    *safe = (k >= mcurrent);
    return 1;
}

int sumtest(int sum[], int ns, int state1[], int ns1, int state2[], int ns2)
{

    int accum, accum1, accum2;
    int i;
    if (ns1 < ns - 1 || ns2 < ns - 1)
        return 0;
    accum = sum[ns - 1];

    accum1 = 0;
    for (i = ns - 1; i < ns1; i++)
        accum1 += state1[i];

    accum2 = 0;
    for (i = ns - 1; i < ns2; i++)
        accum2 += state2[i];

    if (accum > accum1 + accum2)
        return 0;
    for (i = ns - 2; i >= 0; i--)
    {
        accum1 += state1[i];
        accum2 += state2[i];
        if (accum > accum1)
            return 0;
        if (accum > accum2)
            return 0;
        if (sum[i] + 2 * accum > accum1 + accum2)
            return 0;
        accum += sum[i];
    }
    return 1;
}

void addstate(int sum[], int *nsp, int state1[], int ns1, int state2[], int ns2)
{
    int accum[EMAX + 1], accum1[EMAX + 1], accum2[EMAX + 1];
    int ns, i, j, k;
    /* Ensure that output(sum[]) .ge. input(sum[]). */
    ns = *nsp;
    ns = MAX(ns, ns1);
    ns = MAX(ns, ns2);
    accum[ns] = accum1[ns] = accum2[ns] = 0;
    for (i = ns - 1; i >= 0; i--)
    {
        accum[i] = accum[i + 1] + (i < *nsp ? sum[i] : 0);
        accum1[i] = accum1[i + 1] + (i < ns1 ? state1[i] : 0);
        accum2[i] = accum2[i + 1] + (i < ns2 ? state2[i] : 0);
    }
    for (j = ns - 1; j >= 0; j--)
    {
        k = mcurrent;
        k = MIN(k, accum1[j] + accum2[j] - accum[j + 1]);
        if (j > 0)
            k = MIN(k, accum1[j - 1]);
        if (j > 0)
            k = MIN(k, accum2[j - 1]);
        for (i = 0; i < j; i++)
            k = MIN(k, accum1[i] + accum2[i] - accum[i]);
        accum[j] = k;
    }
    while (ns > 0 && accum[ns - 1] == 0)
        ns--;
    *nsp = ns;
    sum[ns - 1] = accum[ns - 1];
    for (j = ns - 2; j >= 0; j--)
    {
        accum[j] = MIN(accum[j], mcurrent);
        sum[j] = accum[j] - accum[j + 1];
    }
    assert(sumtest(sum, ns, state1, ns1, state2, ns2));
}