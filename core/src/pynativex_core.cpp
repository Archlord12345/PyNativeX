#include "pynativex/pynativex_core.h"

#include <new>
#include <vector>

struct PnxEngine {
  PnxEngineConfig config;
  uint64_t last_sequence = 0;
  std::vector<uint8_t> last_operations;
};

PnxResult pnx_engine_create(const PnxEngineConfig* config, PnxEngine** engine) {
  if (config == nullptr || engine == nullptr || config->width_px == 0 ||
      config->height_px == 0 || config->density <= 0) {
    return PNX_INVALID_ARGUMENT;
  }
  if (config->abi_version != PNX_ABI_VERSION) {
    return PNX_UNSUPPORTED_PROTOCOL;
  }
  auto* created = new (std::nothrow) PnxEngine{*config};
  if (created == nullptr) {
    return PNX_INTERNAL_ERROR;
  }
  *engine = created;
  return PNX_OK;
}

void pnx_engine_destroy(PnxEngine* engine) { delete engine; }

PnxResult pnx_engine_apply_operations(
    PnxEngine* engine,
    const uint8_t* operations,
    size_t operations_size,
    uint64_t sequence) {
  if (engine == nullptr || operations == nullptr || operations_size == 0 ||
      sequence <= engine->last_sequence) {
    return PNX_INVALID_ARGUMENT;
  }
  engine->last_operations.assign(operations, operations + operations_size);
  engine->last_sequence = sequence;
  return PNX_OK;
}

uint64_t pnx_engine_last_sequence(const PnxEngine* engine) {
  return engine == nullptr ? 0 : engine->last_sequence;
}
