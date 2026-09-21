#include "pynativex/pynativex_core.h"

#include <cassert>
#include <cstdint>

int main() {
  PnxEngine* engine = nullptr;
  const PnxEngineConfig config{
      .abi_version = PNX_ABI_VERSION,
      .width_px = 720,
      .height_px = 1280,
      .density = 2.0F,
  };
  assert(pnx_engine_create(&config, &engine) == PNX_OK);
  assert(engine != nullptr);

  const uint8_t operations[] = {1, 2, 3};
  assert(pnx_engine_apply_operations(engine, operations, sizeof(operations), 1) == PNX_OK);
  assert(pnx_engine_last_sequence(engine) == 1);
  assert(pnx_engine_apply_operations(engine, operations, sizeof(operations), 1) ==
         PNX_INVALID_ARGUMENT);

  pnx_engine_destroy(engine);
  return 0;
}
