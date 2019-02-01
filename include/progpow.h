/*typedef struct {
    unsigned char data[64];
} secp256k1_pubkey;

typedef union
{
    uint64_t word64s[4];
    uint32_t word32s[8];
    uint8_t bytes[32];
} hash256;

typedef union
{
    uint64_t word64s[8];
    uint32_t word32s[16];
    uint8_t bytes[64];
} hash512;

typedef struct
{
    hash256 final_hash;
    hash256 mix_hash;
} result;

typedef struct
{
    const int epoch_number;
    const int light_cache_num_items;
    const union ethash_hash512* const light_cache;
    const uint32_t* const l1_cache;
    const int full_dataset_num_items;
} epoch_context;

epoch_context* ethash_create_epoch_context(int epoch_number);

result hash(const epoch_context context, const hash256 header_hash, uint64_t nonce);


void ethash_epoch_context_initialise(epoch_context* context, int epoch_number);


void calc_hash( result* res, epoch_context* context, int block_number, hash256* header_hash,
                   uint64_t nonce);
*/

typedef union ethash_hash256
{
    uint64_t word64s[4];
    uint32_t word32s[8];
    uint8_t bytes[32];
} hash256;

typedef union ethash_hash512
{
    uint64_t word64s[8];
    uint32_t word32s[16];
    uint8_t bytes[64];
} hash512;

typedef struct result 
{
    hash256 final_hash;
    hash256 mix_hash;
} result;

typedef struct search_result
{
    uint8_t solution_found;
    uint64_t nonce;
    hash256 final_hash;
    hash256 mix_hash;
} search_result;


#define ETHASH_EPOCH_LENGTH 30000
#define ETHASH_LIGHT_CACHE_ITEM_SIZE 64
#define ETHASH_FULL_DATASET_ITEM_SIZE 128
#define ETHASH_NUM_DATASET_ACCESSES 64

/*typedef struct ethash_epoch_context
{
    const int epoch_number;
    const int light_cache_num_items;
    const hash512* const light_cache;
    const int full_dataset_num_items;
} epoch_context;
*/
typedef struct ethash_epoch_context epoch_context;
int ethash_calculate_light_cache_num_items(int epoch_number);

epoch_context* ethash_create_epoch_context(int epoch_number);
void ethash_destroy_epoch_context(epoch_context* context);
void ethash_hash(result* res, epoch_context* context, hash256* header_hash, uint64_t nonce);
void ethash_search_light_till_result(result* res, epoch_context* context, hash256* header_hash, hash256* boundary, uint64_t* start_nonce);
void progpow_hash(result* res, epoch_context* context, int block_number, hash256* header_hash,  uint64_t nonce); 
void progpow_search_light(search_result* res, epoch_context* context, int block_number,
   hash256* header_hash, hash256* boundary, uint64_t start_nonce, size_t iterations);
void hash256_serialize(hash256* h, char* output);
void hash256_parse(hash256* h, char* input);
void result_serialize(result * r, char* output);
void epoch_context_parse(epoch_context* ctx, int* epoch_number, int* light_cache_num_items, int* full_dataset_num_items);

