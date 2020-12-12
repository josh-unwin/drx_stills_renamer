# DRX STILLS RENAMER

This tool takes arguments of either:
* One directory
* A list of files (all files must come from the same directory)

It will look for .drx files produced from Davinci Resolve and use the data within to:
1. Rename both the .drx and related still image to `REELNAME___srctc_TCOFSTILL`
2. Generate EDLs of the stills, one per roll number (first 4 characters of REELNAME)


### Written in Python3 by Josh Unwin

-----------------------------

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
