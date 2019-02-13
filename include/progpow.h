#define ETHASH_EPOCH_LENGTH 30000
#define ETHASH_LIGHT_CACHE_ITEM_SIZE 64
#define ETHASH_FULL_DATASET_ITEM_SIZE 128
#define ETHASH_NUM_DATASET_ACCESSES 64


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


typedef struct ethash_epoch_context epoch_context;

int ethash_calculate_light_cache_num_items(int epoch_number);
epoch_context* ethash_create_epoch_context(int epoch_number);
void ethash_destroy_epoch_context(epoch_context* context);
void ethash_hash(result* res, epoch_context* context, hash256* header_hash, uint64_t nonce);
void ethash_search_light_till_result(result* res, epoch_context* context, hash256* header_hash, hash256* boundary, uint64_t* start_nonce);
void progpow_hash(result* res, epoch_context* context, int block_number, hash256* header_hash,  uint64_t nonce); 
void progpow_search_light(search_result* res, epoch_context* context, int block_number,
   hash256* header_hash, hash256* boundary, uint64_t start_nonce, size_t iterations);

