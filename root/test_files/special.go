
// This is the special file
// and there is a file comment documentation
// Соблюдать такой же порядок, что и в файле
// Везде, где применяется импорт - нужно его выводить
// А так то просто надо вывести какие импорты юзаются и все

// Еще парочку

// Еееще парочку, в очередь @#$! дети

/*
Опача, а тут оказывается, что это тоже входит в овервью файла.
Даа, коменты уже были.
Дааааа, многострочный комментарий.

Даже пустые линии могут быть.
Но к счастью всегда слэш-звездочка отдельными строчками
*/

// Comment for imported package
// Импорты дальше не комментируются впринципе, но перечисляются
package whatever_commented


import (
	"internal/bytealg"
	"unicode"
)

// But there are several imports
var lolkek = 1

import (
	"unicode/utf8"
)

// Такие константы тоже выводятся, если с комментариями
// Если их нет - полностью игнорируются
// Потому следуюющие должны быть пропущены
// И коментарии внутри тоже игнорируются
const (
	Store   uint16 = 0 // no compression
)

// Если их несколько - обьединяем в один, вместе с одиночными
const (
	Store   uint16 = 0 // no compression
)

const (
	Deflate uint16 = 8 // DEFLATE compressed
)

// Все что было сказано о константах - работает с переменными
var (
	Store   uint16 = 1 // no compression
)
// И тут тоже
// Следующие тоже пропускаются
var (
	Store   uint16 = 2 // no compression
)

var (
	Store   uint16 = 3 // no compression
)


// Random documented function.
// factor for use in Rabin-Karp algorithm.
func hashStr(sep string) (uint32, uint32) {
	hash := uint32(0)
	for i := 0; i < len(sep); i++ {
		hash = hash*primeRK + uint32(sep[i])
	}
	// There is usage of imports
	fmt.Println(unicode.IsSpace(1))
	return hash
}

func notDocumentedFunction(i string) (string) {
    return SurprizeMotherFucker
}

// documented constant
const primeRK = 16777619

const notDocumentedConstant

// documented variable
var whateverVariable
var notDocumentedVariable

// Такой штукой мы просто определяем тип данных, который состоит из других данных
// А ля композиция
// Виводить его надо полностью, увы
// Но в Голанге нет классов, а внутри тайпов не метододв и конструкторов
// oooooooooooooou yeaaaaah!!!!
type CustomType struct {
    one string
    // Переменные тоже комментируются, предыдущее упущено нарочно
    two string
    // Типы всегда указываются
    three string
}

// все, финишь, конец, финито, кончита, зе енд
var PleaseGiveMeMaxMarkMisterTerletskiy