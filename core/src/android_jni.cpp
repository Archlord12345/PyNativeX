#include "pynativex/pynativex_core.h"

#include <android/native_window.h>
#include <android/native_window_jni.h>
#include <jni.h>

#include <cstdint>

namespace {
jlong create_engine(JNIEnv* env, jobject, jobject surface, jfloat density) {
  ANativeWindow* window = ANativeWindow_fromSurface(env, surface);
  if (window == nullptr) {
    return 0;
  }
  const PnxEngineConfig config{
      .abi_version = PNX_ABI_VERSION,
      .width_px = static_cast<uint32_t>(ANativeWindow_getWidth(window)),
      .height_px = static_cast<uint32_t>(ANativeWindow_getHeight(window)),
      .density = density,
  };
  ANativeWindow_release(window);
  PnxEngine* engine = nullptr;
  return pnx_engine_create(&config, &engine) == PNX_OK
             ? reinterpret_cast<jlong>(engine)
             : 0;
}

void resize_engine(JNIEnv*, jobject, jlong, jint, jint) {
  // Surface metrics become a versioned engine event in the next milestone.
}

void vsync_engine(JNIEnv*, jobject, jlong, jlong) {
  // The phase-one renderer will schedule raster work from this callback.
}

void destroy_engine(JNIEnv*, jobject, jlong handle) {
  pnx_engine_destroy(reinterpret_cast<PnxEngine*>(handle));
}
}  // namespace

JNIEXPORT jint JNI_OnLoad(JavaVM* vm, void*) {
  JNIEnv* env = nullptr;
  if (vm->GetEnv(reinterpret_cast<void**>(&env), JNI_VERSION_1_6) != JNI_OK) {
    return JNI_ERR;
  }
  jclass activity = env->FindClass("dev/pynativex/android/PyNativeXActivity");
  if (activity == nullptr) {
    return JNI_ERR;
  }
  const JNINativeMethod methods[] = {
      {"nativeCreateEngine", "(Ljava/lang/Object;F)J", reinterpret_cast<void*>(create_engine)},
      {"nativeResize", "(JII)V", reinterpret_cast<void*>(resize_engine)},
      {"nativeVsync", "(JJ)V", reinterpret_cast<void*>(vsync_engine)},
      {"nativeDestroyEngine", "(J)V", reinterpret_cast<void*>(destroy_engine)},
  };
  if (env->RegisterNatives(activity, methods, sizeof(methods) / sizeof(methods[0])) != JNI_OK) {
    return JNI_ERR;
  }
  return JNI_VERSION_1_6;
}
