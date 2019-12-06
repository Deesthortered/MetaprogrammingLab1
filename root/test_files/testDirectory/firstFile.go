// ToTitle returns a copy of the string s with all Unicode letters mapped to
// their Unicode title case.
func ToTitle(s string) string { return Map(unicode.ToTitle, s) }

// ToUpperSpecial returns a copy of the string s with all Unicode letters mapped to their
// upper case using the case mapping specified by c.
func ToUpperSpecial(c unicode.SpecialCase, s string) string {
	return Map(c.ToUpper, s)
}