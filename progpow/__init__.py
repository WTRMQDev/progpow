from ._libprogpow0_9_2 import ffi as ffi0_9_2, lib as lib0_9_2
from collections import OrderedDict

class ProgPowHandler:
  def __init__(self, max_contexts_num=1, version=None):
    if not version:
      warnings.warn("Default progpow versioning is deprecated. Version should be set explicitly", DeprecationWarning)
      version='0.9.2'
    self.version = version
    self.ffi, self.lib = ffi0_9_2, lib0_9_2
    self.max_contexts_num = max_contexts_num
    self.contexts=OrderedDict()

  def bytes_to_hash256(self, bts):
    hash256 = self.ffi.new("hash256*")
    for i in range(32):
      hash256.bytes[i]=bts[i]
    return hash256

  def get_epoch_num(self, block_num):
    return block_num//self.lib.ETHASH_EPOCH_LENGTH

  def _create_context(self, epoch_num):
    ctx = lib.ethash_create_epoch_context(epoch_num)
    self.contexts[epoch_num]=ctx

  def _destroy_oldest_context(self):
    epoch_num, ctx = self.contexts.popitem(0)
    lib.ethash_destroy_epoch_context(ctx)
 
  def _check_context(self, epoch_num):
    if epoch_num in self.contexts:
      return
    self._create_context(epoch_num)
    while len(self.contexts)>self.max_contexts_num:
      self._destroy_oldest_context()

  def hash_result(self, header_height, header_hash, nonce):
    hh = self.bytes_to_hash256(header_hash)
    result = self.ffi.new("result*")
    epoch_num = self.get_epoch_num(header_height)
    self._check_context(epoch_num)
    self.lib.progpow_hash(result, self.contexts[epoch_num], header_height, hh,  nonce) 
    return bytes(result.mix_hash.bytes), bytes(result.final_hash.bytes)

  def hash(self, header_height, header_hash, nonce):
    return self.hash_result(header_height, header_hash, nonce)[1]
    
  def light_search(self, header_height, header_hash, target, start_nonce = 0, iterations=0, step = 2**10):
    hh = bytes_to_hash256(header_hash)
    boundary = bytes_to_hash256(target)
    search_result = ffi.new("search_result*")
    epoch_num = get_epoch_num(header_height)
    self._check_context(epoch_num)
    nonce = start_nonce
    max_nonce = start_nonce+iterations
    while nonce<max_nonce:
      next_iter = step if nonce+step<max_nonce else max_nonce-nonce
      lib.progpow_search_light(search_result, self.contexts[epoch_num], header_height, hh, boundary, start_nonce, next_iter)
      nonce+=next_iter
      if search_result.solution_found:
        break
    if search_result.solution_found:
      return {'solution_found':True, 'nonce':search_result.nonce, 'final_hash':bytes(search_result.final_hash.bytes)}
    else:
      return {'solution_found':False}

  def give_seed(self, header_height):
    seed = ffi.new("hash256*")
    lib.ethash_initialise_epoch_seed(seed, get_epoch_num(header_height))
    return bytes(seed.bytes)

  def get_epoch_by_seed(self, seed):
    seed_hash = bytes_to_hash256(seed)
    return lib.find_epoch_number_by_seed(seed_hash)

  def __del__(self):
    while len(self.contexts):
      self._destroy_oldest_context()
