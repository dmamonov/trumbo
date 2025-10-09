plugins {
    kotlin("jvm") version "2.1.10"
}

group = "com.teya"
version = "unspecified"

repositories {
    mavenCentral()
}

dependencies {
    testImplementation(kotlin("test"))
}

tasks.test {
    useJUnitPlatform()
}