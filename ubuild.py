build.packages.install("uranium-plus")
import uranium_plus

build.config.update({
    "uranium-plus": {
        "module": "jsonschema_extractor"
    }
})

uranium_plus.bootstrap(build)