#ifndef PYNATIVEX_CORE_H
#define PYNATIVEX_CORE_H

#include <stddef.h>
#include <stdint.h>

#if defined(_WIN32)
#define PNX_EXPORT __declspec(dllexport)
#else
#define PNX_EXPORT __attribute__((visibility("default")))
#endif

#ifdef __cplusplus
extern "C" {
#endif

#define PNX_ABI_VERSION 1

typedef struct PnxEngine PnxEngine;

typedef enum PnxResult {
  PNX_OK = 0,
  PNX_INVALID_ARGUMENT = 1,
  PNX_UNSUPPORTED_PROTOCOL = 2,
  PNX_INTERNAL_ERROR = 3
} PnxResult;

typedef struct PnxEngineConfig {
  uint32_t abi_version;
  uint32_t width_px;
  uint32_t height_px;
  float density;
} PnxEngineConfig;

PNX_EXPORT PnxResult pnx_engine_create(const PnxEngineConfig* config, PnxEngine** engine);
PNX_EXPORT void pnx_engine_destroy(PnxEngine* engine);
PNX_EXPORT PnxResult pnx_engine_apply_operations(
    PnxEngine* engine,
    const uint8_t* operations,
    size_t operations_size,
    uint64_t sequence);
PNX_EXPORT uint64_t pnx_engine_last_sequence(const PnxEngine* engine);

#ifdef __cplusplus
}
#endif

#endif
