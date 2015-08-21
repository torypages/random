// https://www.youtube.com/watch?v=rDPuaNw9_Eo
// String matching Boyer Moore's and Horspool Algorithm

// Can I make this functional?

object MyObject{
  def main(args: Array[String]): Unit = {
    val haystack: Array[Char] = "jim_saw_me_in_a_barbrr_parlour".toCharArray
    val needle: Array[Char] = "barber".toCharArray
    val needleLen = needle.length

    def rightMostLessLast(haystack: Array[Char], needle: Char): Int = {
      for (i <- haystack.length - 1 - 1 to 0 by -1) {
        val currentChar = haystack(i)
        if (currentChar == needle)
          return i
      }
      0
    }

    val shiftMap: Map[Char, Int] = (for (i <- 0 to needleLen - 1)
      yield (needle(i) -> (needleLen - 1 - rightMostLessLast(needle, needle(i))))).toMap

    def search: Boolean = {
      var startWindow = 0
      while (startWindow + needleLen < haystack.length) {
        var iHaystack = startWindow + needleLen - 1
        var iNeedle = needleLen - 1
        while (iNeedle != -1 && (needle(iNeedle) == haystack(iHaystack))) {
          iHaystack = iHaystack - 1
          iNeedle = iNeedle - 1
        }
        if (iNeedle == -1)
          return true
        val shift = shiftMap.getOrElse(haystack(startWindow + needleLen - 1), needleLen)
        startWindow = startWindow + shift
      }
      return false
    }

    println(search)
  }
}
