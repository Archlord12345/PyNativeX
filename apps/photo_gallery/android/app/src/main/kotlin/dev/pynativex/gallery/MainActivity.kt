package dev.pynativex.gallery

import android.app.Activity
import android.content.Context
import android.graphics.Color
import android.graphics.Outline
import android.graphics.drawable.GradientDrawable
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.Gravity
import android.view.MotionEvent
import android.view.View
import android.view.ViewGroup
import android.view.ViewOutlineProvider
import android.view.Window
import android.view.WindowInsets
import android.widget.Button
import android.widget.FrameLayout
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import org.json.JSONObject

private class AccessibleGalleryImage(context: Context) : ImageView(context) {
    override fun performClick(): Boolean {
        super.performClick()
        return true
    }
}

private data class GallerySpec(
    val applicationTitle: String,
    val eyebrow: String,
    val introduction: String,
    val assets: List<String>,
    val titles: List<String>,
    val captions: List<String>,
    val autoPlaySeconds: Int,
)

private object PyNativeXProtocol {
    fun load(activity: Activity): GallerySpec {
        val document = activity.assets.open("gallery_ui.json")
            .bufferedReader()
            .use { JSONObject(it.readText()) }
        val applicationTitle = document
            .getJSONObject("application")
            .getString("title")
        val operations = document.getJSONArray("operations")
        var gallery: JSONObject? = null
        val textNodes = mutableListOf<String>()
        for (index in 0 until operations.length()) {
            val operation = operations.getJSONObject(index)
            if (operation.getString("code") != "create") continue
            val payload = operation.getJSONObject("payload")
            if (payload.getString("type") == "Text") {
                textNodes += payload.getJSONObject("props").getString("value")
            }
            if (payload.getString("type") == "PhotoGallery") {
                gallery = payload.getJSONObject("props")
            }
        }
        requireNotNull(gallery) { "Python UI does not contain a PhotoGallery widget" }
        require(textNodes.size >= 3) { "Python UI must provide title, eyebrow and introduction" }
        return GallerySpec(
            applicationTitle = applicationTitle,
            eyebrow = textNodes[textNodes.lastIndex - 1],
            introduction = textNodes.last(),
            assets = gallery.getJSONArray("assets").toStringList(),
            titles = gallery.getJSONArray("titles").toStringList(),
            captions = gallery.getJSONArray("captions").toStringList(),
            autoPlaySeconds = gallery.getInt("auto_play_seconds"),
        )
    }

    private fun org.json.JSONArray.toStringList(): List<String> =
        List(length()) { getString(it) }
}

class MainActivity : Activity() {
    private lateinit var spec: GallerySpec
    private lateinit var photo: ImageView
    private lateinit var title: TextView
    private lateinit var caption: TextView
    private lateinit var counter: TextView
    private lateinit var indicators: LinearLayout
    private lateinit var playButton: Button
    private val handler = Handler(Looper.getMainLooper())
    private var currentIndex = 0
    private var autoPlay = true
    private var touchStartX = 0f

    private val advance = object : Runnable {
        override fun run() {
            if (autoPlay) showPhoto((currentIndex + 1) % spec.assets.size)
            scheduleAdvance()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.requestFeature(Window.FEATURE_NO_TITLE)
        window.statusBarColor = Color.rgb(2, 6, 23)
        window.navigationBarColor = Color.rgb(2, 6, 23)
        spec = PyNativeXProtocol.load(this)
        currentIndex = savedInstanceState?.getInt("photo_index") ?: 0
        setContentView(buildInterface())
        showPhoto(currentIndex, animate = false)
    }

    override fun onResume() {
        super.onResume()
        scheduleAdvance()
    }

    override fun onPause() {
        handler.removeCallbacks(advance)
        super.onPause()
    }

    override fun onSaveInstanceState(outState: Bundle) {
        outState.putInt("photo_index", currentIndex)
        super.onSaveInstanceState(outState)
    }

    private fun buildInterface(): View {
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(dp(20), dp(18), dp(20), dp(16))
            setBackgroundColor(Color.rgb(2, 6, 23))
            setOnApplyWindowInsetsListener { view, insets ->
                val top = if (android.os.Build.VERSION.SDK_INT >= 30) {
                    insets.getInsets(WindowInsets.Type.statusBars()).top
                } else {
                    @Suppress("DEPRECATION")
                    insets.systemWindowInsetTop
                }
                view.setPadding(dp(20), top + dp(12), dp(20), dp(16))
                insets
            }
        }

        root.addView(TextView(this).apply {
            text = spec.eyebrow
            setTextColor(Color.rgb(56, 189, 248))
            textSize = 12f
            letterSpacing = 0.16f
            typeface = android.graphics.Typeface.DEFAULT_BOLD
        }, matchWrap())

        root.addView(TextView(this).apply {
            text = spec.applicationTitle
            setTextColor(Color.WHITE)
            textSize = 30f
            typeface = android.graphics.Typeface.DEFAULT_BOLD
            setPadding(0, dp(4), 0, dp(2))
        }, matchWrap())

        root.addView(TextView(this).apply {
            text = spec.introduction
            setTextColor(Color.rgb(148, 163, 184))
            textSize = 14f
            setPadding(0, 0, 0, dp(16))
        }, matchWrap())

        val frame = FrameLayout(this).apply {
            background = roundedBackground(Color.rgb(15, 23, 42), 24f)
            clipToOutline = true
            outlineProvider = roundedOutline(24f)
            minimumHeight = dp(360)
        }
        root.addView(
            frame,
            LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                0,
                1f,
            ),
        )

        photo = AccessibleGalleryImage(this).apply {
            scaleType = ImageView.ScaleType.CENTER_CROP
            isClickable = true
            setOnTouchListener { _, event ->
                when (event.actionMasked) {
                    MotionEvent.ACTION_DOWN -> {
                        touchStartX = event.x
                        true
                    }
                    MotionEvent.ACTION_UP -> {
                        val distance = event.x - touchStartX
                        if (kotlin.math.abs(distance) > dp(48)) {
                            showPhoto(
                                if (distance < 0) {
                                    (currentIndex + 1) % spec.assets.size
                                } else {
                                    (currentIndex - 1 + spec.assets.size) % spec.assets.size
                                },
                            )
                        } else {
                            performClick()
                        }
                        true
                    }
                    else -> true
                }
            }
        }
        frame.addView(photo, matchMatch())

        val overlay = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.BOTTOM
            setPadding(dp(18), dp(48), dp(18), dp(18))
            background = GradientDrawable(
                GradientDrawable.Orientation.BOTTOM_TOP,
                intArrayOf(0xEE020617.toInt(), 0x00020617),
            )
        }
        frame.addView(
            overlay,
            FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.WRAP_CONTENT,
                Gravity.BOTTOM,
            ),
        )

        val titleLine = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
        }
        overlay.addView(titleLine, matchWrap())

        title = TextView(this).apply {
            setTextColor(Color.WHITE)
            textSize = 22f
            typeface = android.graphics.Typeface.DEFAULT_BOLD
        }
        titleLine.addView(
            title,
            LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f),
        )

        counter = TextView(this).apply {
            setTextColor(Color.WHITE)
            textSize = 12f
            gravity = Gravity.CENTER
            background = roundedBackground(0x6638BDF8, 999f)
            setPadding(dp(10), dp(5), dp(10), dp(5))
        }
        titleLine.addView(counter, wrapWrap())

        caption = TextView(this).apply {
            setTextColor(Color.rgb(203, 213, 225))
            textSize = 14f
            setPadding(0, dp(4), 0, 0)
        }
        overlay.addView(caption, matchWrap())

        indicators = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
            setPadding(0, dp(14), 0, dp(10))
        }
        root.addView(indicators, matchWrap())
        repeat(spec.assets.size) {
            indicators.addView(
                View(this),
                LinearLayout.LayoutParams(dp(22), dp(4)).apply {
                    marginStart = dp(3)
                    marginEnd = dp(3)
                },
            )
        }

        val controls = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER
        }
        root.addView(controls, matchWrap())
        controls.addView(controlButton(getString(R.string.previous)) {
            showPhoto((currentIndex - 1 + spec.assets.size) % spec.assets.size)
        }, weighted())
        playButton = controlButton(getString(R.string.pause)) {
            autoPlay = !autoPlay
            playButton.text = getString(if (autoPlay) R.string.pause else R.string.play)
            scheduleAdvance()
        }
        controls.addView(playButton, weighted().apply {
            marginStart = dp(8)
            marginEnd = dp(8)
        })
        controls.addView(controlButton(getString(R.string.next)) {
            showPhoto((currentIndex + 1) % spec.assets.size)
        }, weighted())

        return root
    }

    private fun showPhoto(index: Int, animate: Boolean = true) {
        currentIndex = index
        val resource = imageResource(spec.assets[index])

        val applyPhoto = {
            photo.setImageResource(resource)
            photo.contentDescription = getString(
                R.string.photo_content_description,
                spec.titles[index],
                spec.captions[index],
            )
            title.text = spec.titles[index]
            caption.text = spec.captions[index]
            counter.text = getString(R.string.photo_counter, index + 1, spec.assets.size)
            updateIndicators()
        }
        if (animate) {
            photo.animate()
                .alpha(0.15f)
                .scaleX(1.05f)
                .scaleY(1.05f)
                .setDuration(180)
                .withEndAction {
                    applyPhoto()
                    photo.animate()
                        .alpha(1f)
                        .scaleX(1f)
                        .scaleY(1f)
                        .setDuration(520)
                        .start()
                }
                .start()
        } else {
            applyPhoto()
        }
        scheduleAdvance()
    }

    private fun updateIndicators() {
        for (index in 0 until indicators.childCount) {
            indicators.getChildAt(index).background = roundedBackground(
                if (index == currentIndex) Color.rgb(56, 189, 248) else Color.rgb(51, 65, 85),
                999f,
            )
        }
    }

    private fun scheduleAdvance() {
        handler.removeCallbacks(advance)
        if (autoPlay && spec.autoPlaySeconds > 0) {
            handler.postDelayed(advance, spec.autoPlaySeconds * 1000L)
        }
    }

    private fun imageResource(asset: String): Int = when (asset) {
        "mount_cameroon" -> R.drawable.mount_cameroon
        "limbe_beach" -> R.drawable.limbe_beach
        "rainforest" -> R.drawable.rainforest
        else -> error("Unsupported gallery asset: $asset")
    }

    private fun controlButton(label: String, action: () -> Unit) = Button(this).apply {
        text = label
        isAllCaps = false
        textSize = 12f
        setTextColor(Color.WHITE)
        background = roundedBackground(Color.rgb(15, 23, 42), 14f, Color.rgb(51, 65, 85))
        setPadding(dp(8), 0, dp(8), 0)
        setOnClickListener { action() }
    }

    private fun roundedBackground(color: Int, radius: Float, stroke: Int? = null) =
        GradientDrawable().apply {
            shape = GradientDrawable.RECTANGLE
            cornerRadius = dp(radius.toInt()).toFloat()
            setColor(color)
            if (stroke != null) setStroke(dp(1), stroke)
        }

    private fun roundedOutline(radius: Float) = object : ViewOutlineProvider() {
        override fun getOutline(view: View, outline: Outline) {
            outline.setRoundRect(0, 0, view.width, view.height, dp(radius.toInt()).toFloat())
        }
    }

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density).toInt()
    private fun matchWrap() = LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT,
        ViewGroup.LayoutParams.WRAP_CONTENT,
    )
    private fun matchMatch() = FrameLayout.LayoutParams(
        ViewGroup.LayoutParams.MATCH_PARENT,
        ViewGroup.LayoutParams.MATCH_PARENT,
    )
    private fun wrapWrap() = LinearLayout.LayoutParams(
        ViewGroup.LayoutParams.WRAP_CONTENT,
        ViewGroup.LayoutParams.WRAP_CONTENT,
    )
    private fun weighted() = LinearLayout.LayoutParams(0, dp(48), 1f)
}
