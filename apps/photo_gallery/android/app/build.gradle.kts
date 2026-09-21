import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "dev.pynativex.gallery"
    compileSdk = 36

    defaultConfig {
        applicationId = "dev.pynativex.gallery"
        minSdk = 24
        targetSdk = 36
        versionCode = 1
        versionName = "0.1.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro",
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

}

kotlin {
    compilerOptions {
        jvmTarget.set(JvmTarget.JVM_17)
    }
}

val repoRoot = rootProject.projectDir.resolve("../../..")

val materializeBinaries by tasks.registering(Exec::class) {
    description = "Restores photos and the Gradle wrapper JAR when they are stored as text parts."
    workingDir = repoRoot
    commandLine("python3", "scripts/materialize_binaries.py")
}

val generatePyNativeXUi by tasks.registering(Exec::class) {
    description = "Compiles the Python UI tree into the PyNativeX protocol asset."
    workingDir = rootProject.projectDir
    commandLine(
        "python3",
        "../generate_ui.py",
        "--output",
        "app/src/main/assets/gallery_ui.json",
    )
    dependsOn(materializeBinaries)
}

tasks.named("preBuild") {
    dependsOn(generatePyNativeXUi)
}
