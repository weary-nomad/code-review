import io.ktor.application.*
import io.ktor.http.*
import io.ktor.http.content.*
import io.ktor.request.*
import io.ktor.response.*
import io.ktor.routing.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*
import java.awt.image.BufferedImage
import java.io.File
import java.util.regex.Pattern
import javax.imageio.ImageIO

fun main() {
    /* Pretend this is integrated with Apache and not its own server for this challenge. Usually we'd need to add other configurations to get Netty to work with Apache */
    embeddedServer(Netty, port = 8080) {
        routing {
            post("/imageCheck") {
                val multipart = call.receiveMultipart()
                var fileName: String? = null
                var fileBytes: ByteArray? = null

                multipart.forEachPart { part ->
                    if (part is PartData.FileItem) {
                        fileName = part.originalFileName
                        fileBytes = part.streamProvider().readBytes()
                    }
                    part.dispose()
                }

                if (fileName == null || fileBytes == null) {
                    call.respond(HttpStatusCode.BadRequest, "No file provided")
                    return@post
                }
                
                val filenameRegex = Regex("^.*.jpg$", RegexOption.IGNORE_CASE)
                if (!filenameRegex.matches(fileName!!)) {
                    call.respond(HttpStatusCode.BadRequest, "Invalid filename. Use only letters, numbers, and '.jpg' extension.")
                    return@post
                }

                val image: BufferedImage? = try {
                    ImageIO.read(fileBytes!!.inputStream())
                } catch (e: Exception) {
                    null
                }

                if (image == null) {
                    call.respond(HttpStatusCode.BadRequest, "File is not a valid JPEG image.")
                    return@post
                }

                val uploadPath = File("/var/www/html/uploads/$fileName")
                uploadPath.writeBytes(fileBytes!!)

                val width = image.width
                val height = image.height
                val sizeBytes = fileBytes!!.size

                call.respondText(
                    """
                    Valid JPEG<br>
                    File size: $sizeBytes bytes<br>
                    Dimensions: $width x $height<br>
                    <a href="/uploads/$fileName" target="_blank">View uploaded file</a>
                    """.trimIndent(), ContentType.Text.Html
                )
            }
        }
    }.start(wait = true)
}
