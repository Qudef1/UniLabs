#include "set.h"
#include <UnitTest++/UnitTest++.h>
#include <memory>

TEST(constructorTest1) {
    set s1;
    CHECK_EQUAL(0, s1.get_size());
    CHECK(s1.is_null());
}
TEST(constructorTest2){
    set s = {1,2};
    CHECK(s.contains(1));
    CHECK(s.contains(2));
    CHECK_EQUAL(2,s.get_size());
}
TEST(constructorTest3){
    set s1 = set("{1,2,3,4}");
    std::string temp = "{1,2,3,4}";
    set s2 = set(temp);
    CHECK(s1==s2);
}
TEST(ParseTest){
    CHECK_THROW(set("{1,2,{}"),std::runtime_error);
    CHECK_THROW(set(""),std::runtime_error);
    CHECK_THROW(set("{"),std::runtime_error);
    CHECK_THROW(set("}"),std::runtime_error);
    CHECK_THROW(set("1"),std::runtime_error);
    CHECK_THROW(set(" "),std::runtime_error);

}
TEST(UnionTest){
    set s1("{1,2,3,{1,2},{1},{}}");
    set s2("{1,2,3,4,{1,2,3},{2},{}}");
    set s3("{1,2,3,4,{1,2,3},{1,2},{1},{2},{}}");
    CHECK(s1+s2==s3);
}
TEST(IntersectionTest){
    set s1("{1,2,3,{1,2},{1},{}}");
    set s2("{1,2,3,4,{1,2,3},{2},{}}");
    set s3("{1,2,3,{}}");
    CHECK(s1*s2==s3);
}
TEST(MinusTest){
    set s1("{1,2,3,{1,2},{1},{}}");
    set s2("{1,2,3,4,{1,2,3},{2},{}}");
    set s3("{{1,2},{1}}");
    CHECK((s1-s2)==s3);
}

TEST(SetAddContains) {
    set s;
    s.add(1);
    s.add(2);
    
    CHECK(s.contains(1));
    CHECK(s.contains(2));
    CHECK(!s.contains(3));
    CHECK_EQUAL(2, s.get_size());
}

TEST(SetParseSimple) {
    auto s = set("{1, 2, 3}");
    CHECK_EQUAL(3, s.get_size());
    CHECK(s.contains(1));
    CHECK(s.contains(2));
    CHECK(s.contains(3));
}

TEST(SetParseNested) {
    auto s = set("{1, {2, 3}, 4}");
    CHECK_EQUAL(3, s.get_size()); // 1, {2,3}, 4
}

TEST(SetOperations) {
    set s1 = set(std::string("{1, 2, 3}"));
    set s2 = set(std::string("{3, 4, 5}"));
    
    auto union_set = s1 + s2;
    CHECK_EQUAL(5, union_set.get_size());
    
    auto intersect_set = s1 * s2;
    CHECK_EQUAL(1, intersect_set.get_size());
    CHECK(intersect_set.contains(3));
}

TEST(SetEquality) {
    set s1 = set(std::string("{1, 2, 3}"));
    set s2 = set(std::string("{1, 2, 3}"));
    set s3 = set(std::string("{4, 5, 6}"));
    
    CHECK(s1 == s2);
    CHECK(!(s1 == s3));
}

TEST(SetPrintTest){
    set s = {1,2,3};
    std::stringstream ss;
    ss<<s;
    CHECK_EQUAL("{1, 2, 3}",ss.str());

    set nested = {1,2};
    set s2;
    s2.add(std::make_shared<set>(nested));
    std::stringstream ss2;
    ss2<<s2;
    CHECK(ss2.str().find("{1, 2}")!=std::string::npos);

}
TEST(RemoveTest){
    set s = {1,2,3};
    CHECK(s.remove(2));
    CHECK_EQUAL(2,s.get_size());
    CHECK(!s[2]);

    CHECK(!s[999]);
    CHECK_EQUAL(2,s.get_size());
}
TEST(SetPlusEqualTest){
    set s1("{1,2,3,{1,2},{1},{}}");
    set s2("{1,2,3,4,{1,2,3},{2},{}}");
    set s3("{1,2,3,4,{1,2,3},{1,2},{1},{2},{}}");
    s1+=s2;
    CHECK(s1==s3);
}
TEST(IntersectionEqualTest){
    set s1("{1,2,3,{1,2},{1},{}}");
    set s2("{1,2,3,4,{1,2,3},{2},{}}");
    set s3("{1,2,3,{}}");
    s1*=s2;
    CHECK(s1==s3);
}
TEST(SetMinusEqualTest){
    set s1("{1,2,3,{1,2},{1},{}}");
    set s2("{1,2,3,4,{1,2,3},{2},{}}");
    set s3("{{1,2},{1}}");
    s1-=s2;
    CHECK(s1==s3);
}
TEST(selfUnion){
    set s1("{1,2,3,{1,2},{1},{}}");
    auto s_union = s1+s1;
    CHECK_EQUAL(s1.get_size(),s_union.get_size());
    auto s_intersect = s1*s1;
    CHECK_EQUAL(s1.get_size(),s_intersect.get_size());
    CHECK(s_union==s_intersect);
    auto s_minus = s1-s1;
    CHECK_EQUAL(0,s_minus.get_size());
    CHECK(s_minus.is_null());
}
TEST(BooleanTest){
    set s1("{1,2,{1}}");
    auto boolean_set = s1.boolean();

    CHECK_EQUAL(8,boolean_set.get_size());

    set nested_s1 = {1};
    set nested_s2 = {1,2};
    set nested_s3 = {2};
    CHECK(boolean_set.contains(std::make_shared<set>(nested_s1)));
    CHECK(boolean_set.contains(std::make_shared<set>(nested_s2)));
    CHECK(boolean_set.contains(std::make_shared<set>(nested_s3)));

}
TEST(TestSetEquality2){
    set s1 = {1,2};
    set s2 = {2,1};
    CHECK(s1==s2);
    set ss1;
    ss1.add(std::make_shared<set>(s1));
    set ss2;
    ss2.add(std::make_shared<set>(s2));
    CHECK(ss1==ss2);
}
TEST(AddDuplicates){
    set s1;
    s1.add(1);
    s1.add(1);
    s1.add(2);
    CHECK_EQUAL(2,s1.get_size());
}
TEST(removeDuplicates){
    set s1;
    set nested = {1,2};
    s1.add(1);
    s1.add(std::make_shared<set>(nested));
    s1.add(std::make_shared<set>(nested));
    CHECK_EQUAL(s1.get_size(),2);
    CHECK(s1.remove(1));
    CHECK(!s1.remove(1));
    CHECK(s1.remove(std::make_shared<set>(nested)));
    CHECK(!s1.remove(std::make_shared<set>(nested)));
    CHECK_EQUAL(s1.get_size(),0);
}
TEST(SetNotEqualTest) {
    set s1 = {1, 2};
    set s2 = {1, 2, 3};
    CHECK(s1 != s2);

    set s3 = {1, 2};
    CHECK(!(s1 != s3));
}
int main() {
    return UnitTest::RunAllTests();
}

//g++ -std=c++17 -I/usr/include set.cpp test.cpp -lUnitTest++ -o tests && ./tests
