object MyObject{
  def binarySearch(haystack: List[Int], needle: Int): Option[Int] = {
     def _binarySearch(low: Int, high: Int): Option[Int] = {
       if (low > high) return None
       val midIndex = low + (high - low) / 2
       haystack(midIndex) match {
         case midVal if (midVal == needle) => Some(midIndex)
         case midVal if (midVal <= needle) => _binarySearch(midIndex + 1, high)
         case midVal if (midVal >= needle) => _binarySearch(low, midIndex - 1)
       }
     } 
     _binarySearch(0, haystack.size - 1)
  }
  
  def main(args: Array[String]): Unit = {
    val data = List(1,88,999,333,222,4432,24,657,234,121,45,435,234).sorted
    println(binarySearch(data, 333))
    println(binarySearch(data, 77))
  }
}