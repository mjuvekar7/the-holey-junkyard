/**
 * InputParser.java: parses XML input
 * Copyright (C) 2012 - 2014, 2016 Shardul C.
 *
 * This file is part of VoteCounter.
 *
 * VoteCounter is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * VoteCounter is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with VoteCounter.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Bugs, tips, suggestions, requests to <shardul.chiplunkar@gmail.com>.
 */
package voteserver;

import java.util.ArrayList;
import java.util.List;
import org.jdom2.Element;
import org.jdom2.JDOMException;
import org.jdom2.input.SAXBuilder;

/**
 * XML input parser for VoteCounter.
 *
 * This class provides methods for parsing an XML input file and converting the
 * data into a format usable by VoteCounter.
 *
 * The format of the XML file should be:
 * <pre>
 * {@code
<input>
     <groups>
         <groupname>Blues</groupname>
         <groupname>Greens</groupname>
     </groups>
     <posts>
         <generic>
             <post name="Treasurer">
                 <nominee>Blorb</nominee>
                 <nominee>Cagfrigii</nominee>
                 <nominee>Eowx</nominee>
             </post>
         </generic>
         <nongeneric>
             <post name="Captain">
                 <group name="Blues">
                     <nominee>Plaahy</nominee>
                     <nominee>Nbog</nominee>
                     <nominee>Zkurta</nominee>
                     <nominee>Aqatoto</nominee>
                     <nominee>Xeeml</nominee>
                 </group>
                 <group name="Greens">
                     <nominee>Ynivuj</nominee>
                     <nominee>Fendirwi</nominee>
                     <nominee>Kaalei</nominee>
                     <nominee>Pimklri</nominee>
                 </group>
             </post>
         </nongeneric>
     </posts>
 </input>
 * }
 * </pre>
 *
 * Of course, there can be no groups (or equivalently, a missing {@code
 * <groups>} tag) in which case there cannot be any nongeneric posts. There can
 * be as many groups and posts as desired, with any number of nominees
 * contesting each post; however, it is assumed that all groups independently
 * contest all nongeneric posts.
 *
 * @author shardul
 */
public class InputParser {

    // data to be parsed
    private final List<String> groups = new ArrayList<>();
    private final List<String> genericPosts = new ArrayList<>();
    private final List<List<String>> genericNominees = new ArrayList<>();
    private final List<String> nonGenericPosts = new ArrayList<>();
    private final List<List<List<String>>> nonGenericNominees = new ArrayList<>();

    /**
     * Parse the XML input file and get groups, posts, and nominees.
     *
     * The {@code parse} method parses the document using
     * {@link org.jdom2.input.SAXBuilder} which builds a pseudo-tree structure
     * representing the XML file. The method then traverses each element and
     * builds a representation of the data that makes sense to the vote-counting
     * program; that is, it organizes the data into posts and groups as
     * specified in the input file.
     *
     * The behavior of the {@code parse} method is unspecified if the XML file
     * is not structured as it expects it to be. This can happen even if the
     * syntax is all right, because of mispelings or order elements of incorrect
     * the.
     *
     * @param is an {@link java.io.InputStream} for the XML input file
     * @throws JDOMException if XML structure/syntax is incorrect
     * @throws java.io.IOException if error accessing file
     */
    public void parse(java.io.InputStream is) throws JDOMException, java.io.IOException {
        Element root = ((new SAXBuilder()).build(is)).getRootElement();

        Element child = root.getChild("groups");
        if (child != null) {
            List<Element> groupList = child.getChildren();
            for (int i = 0; i < groupList.size(); i++) {
                groups.add(groupList.get(i).getText());
            }
        }

        child = root.getChild("posts").getChild("generic");
        if (child != null) {
            List<Element> genericPostElements = child.getChildren();
            for (int i = 0; i < genericPostElements.size(); i++) {
                genericPosts.add(genericPostElements.get(i).getAttributeValue("name"));
                genericNominees.add(new ArrayList<String>());
                List<Element> currentNominees = genericPostElements.get(i).getChildren();
                for (int j = 0; j < currentNominees.size(); j++) {
                    genericNominees.get(i).add(currentNominees.get(j).getText());
                }
            }
        }

        child = root.getChild("posts").getChild("nongeneric");
        if (child != null) {
            List<Element> nonGenericPostElements = child.getChildren();
            for (int i = 0; i < nonGenericPostElements.size(); i++) {
                nonGenericPosts.add(nonGenericPostElements.get(i).getAttributeValue("name"));
                nonGenericNominees.add(new ArrayList<List<String>>());
                List<Element> currentGroups = nonGenericPostElements.get(i).getChildren();
                for (int j = 0; j < currentGroups.size(); j++) {
                    nonGenericNominees.get(i).add(new ArrayList<String>());
                    List<Element> currentNominees = currentGroups.get(j).getChildren();
                    for (int k = 0; k < currentNominees.size(); k++) {
                        nonGenericNominees.get(i).get(j).add(currentNominees.get(k).getText());
                    }
                }
            }
        }
    }

    /**
     * Get nominees for generic posts.
     *
     * The return value is a two-dimensional list, with the first dimension
     * representing posts and the second, individual nominees.
     *
     * @return nominees for generic posts
     */
    public List<List<String>> getGenericNominees() {
        return genericNominees;
    }

    /**
     * Get nominees for non-generic posts.
     *
     * The return value is a three-dimensional list, with the first dimension
     * representing posts, the second, groups, and the third, individual
     * nominees.
     *
     * @return nominees for non-generic posts
     */
    public List<List<List<String>>> getNonGenericNominees() {
        return nonGenericNominees;
    }

    /**
     * Get list of nominee groups.
     *
     * @return list of nominee groups
     */
    public List<String> getGroups() {
        return groups;
    }

    /**
     * Get list of generic (non-group) posts.
     *
     * @return list of generic posts
     */
    public List<String> getGenericPosts() {
        return genericPosts;
    }

    /**
     * Get list of non-generic (group-wise) posts.
     *
     * @return list of non-generic posts
     */
    public List<String> getNonGenericPosts() {
        return nonGenericPosts;
    }
}
