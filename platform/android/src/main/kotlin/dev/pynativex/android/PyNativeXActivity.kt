package dev.pynativex.android

import android.os.Bundle
import android.view.Choreographer
import android.view.SurfaceHolder
import android.view.SurfaceView
import androidx.activity.ComponentActivity

/**
 * Minimal Android host for the native engine.
 *
 * Rendering stays in C++; this host owns lifecycle, SurfaceView and vsync.
 */
open class PyNativeXActivity : ComponentActivity(), SurfaceHolder.Callback,
    Choreographer.FrameCallback {
    private lateinit var surfaceView: SurfaceView
    private var engineHandle: Long = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        surfaceView = SurfaceView(this)
        surfaceView.holder.addCallback(this)
        setContentView(surfaceView)
    }

    override fun surfaceCreated(holder: SurfaceHolder) {
        engineHandle = nativeCreateEngine(
            holder.surface,
            resources.displayMetrics.density,
        )
        Choreographer.getInstance().postFrameCallback(this)
    }

    override fun surfaceChanged(holder: SurfaceHolder, format: Int, width: Int, height: Int) {
        nativeResize(engineHandle, width, height)
    }

    override fun surfaceDestroyed(holder: SurfaceHolder) {
        Choreographer.getInstance().removeFrameCallback(this)
        nativeDestroyEngine(engineHandle)
        engineHandle = 0
    }

    override fun doFrame(frameTimeNanos: Long) {
        if (engineHandle != 0L) {
            nativeVsync(engineHandle, frameTimeNanos)
            Choreographer.getInstance().postFrameCallback(this)
        }
    }

    private external fun nativeCreateEngine(surface: Any, density: Float): Long
    private external fun nativeResize(engine: Long, width: Int, height: Int)
    private external fun nativeVsync(engine: Long, frameTimeNanos: Long)
    private external fun nativeDestroyEngine(engine: Long)

    companion object {
        init {
            System.loadLibrary("pynativex_core")
        }
    }
}
